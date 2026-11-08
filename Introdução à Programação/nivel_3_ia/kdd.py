"""kdd.py – funções reutilizáveis para as fases do processo KDD.

Seleção → Limpeza → Transformação → Redução → Mineração → Avaliação

Faz parte do tutorial «Introdução ao Python» (nível IA, módulo 3). Copia este
ficheiro para a pasta do teu projeto e adapta-o: as funções são pequenas de
propósito, para se poderem ler, testar e alterar.
"""
from __future__ import annotations

import unicodedata

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

__all__ = [
    "diagnosticar",
    "normalizar_texto",
    "uniformizar_categorias",
    "remover_duplicados",
    "invalidar_fora_do_intervalo",
    "outliers_iqr",
    "colunas_redundantes",
    "construir_preprocessamento",
    "comparar_modelos",
    "lift_por_decil",
]


# ------------------------------------------------------------------ 2. Limpeza
def diagnosticar(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por coluna: tipo, valores em falta, valores distintos e exemplos."""
    resumo = pd.DataFrame({
        "tipo": df.dtypes.astype(str),
        "em_falta": df.isna().sum(),
        "pct_falta": (df.isna().mean() * 100).round(1),
        "distintos": df.nunique(dropna=True),
        "exemplos": [df[c].dropna().unique()[:4].tolist() for c in df.columns],
    })
    print(f"{len(df)} linhas × {df.shape[1]} colunas | linhas duplicadas: {df.duplicated().sum()}")
    return resumo


def normalizar_texto(serie: pd.Series, acentos: bool = True) -> pd.Series:
    """Tira espaços nas pontas, põe em minúsculas e (opcionalmente) mantém ou remove acentos."""
    # map(str) em vez de astype("string"): os valores em falta continuam NaN (e não pd.NA),
    # que é o que o scikit-learn espera
    s = serie.map(lambda t: t if pd.isna(t) else str(t)).str.strip().str.lower()
    if not acentos:
        s = s.map(lambda t: t if pd.isna(t) else
                  "".join(ch for ch in unicodedata.normalize("NFKD", t) if not unicodedata.combining(ch)))
    return s


def uniformizar_categorias(serie: pd.Series, mapa: dict[str, str] | None = None) -> pd.Series:
    """Normaliza o texto e aplica um dicionário de correspondências (forma normalizada → valor final)."""
    s = normalizar_texto(serie, acentos=False)
    if mapa:
        s = s.replace(mapa)
    return s


def remover_duplicados(df: pd.DataFrame, chave: str | list[str] | None = None) -> pd.DataFrame:
    """Remove linhas repetidas (por todas as colunas ou pela chave) e diz quantas saíram."""
    antes = len(df)
    limpo = df.drop_duplicates(subset=chave, keep="first").reset_index(drop=True)
    print(f"Duplicados removidos: {antes - len(limpo)} (ficam {len(limpo)} linhas)")
    return limpo


def invalidar_fora_do_intervalo(df: pd.DataFrame, regras: dict[str, tuple[float, float]]) -> pd.DataFrame:
    """Substitui por NaN os valores fora de [mínimo, máximo] de cada coluna. Não altera o original."""
    df = df.copy()
    for coluna, (minimo, maximo) in regras.items():
        fora = ~df[coluna].between(minimo, maximo) & df[coluna].notna()
        print(f"{coluna}: {fora.sum()} valores fora de [{minimo}, {maximo}] → NaN")
        df.loc[fora, coluna] = np.nan
    return df


def outliers_iqr(serie: pd.Series, k: float = 1.5) -> pd.Series:
    """Máscara booleana dos valores fora de [Q1 − k·IQR, Q3 + k·IQR] (regra de Tukey)."""
    q1, q3 = serie.quantile([0.25, 0.75])
    iqr = q3 - q1
    return (serie < q1 - k * iqr) | (serie > q3 + k * iqr)


# ------------------------------------------------------------------ 4. Redução
def colunas_redundantes(df: pd.DataFrame, limite: float = 0.95) -> list[str]:
    """Colunas numéricas constantes ou com |correlação| > limite com uma coluna anterior."""
    num = df.select_dtypes("number")
    constantes = [c for c in num.columns if num[c].nunique(dropna=True) <= 1]
    corr = num.drop(columns=constantes).corr().abs()
    superior = corr.where(np.triu(np.ones(corr.shape, dtype=bool), k=1))
    correlacionadas = [c for c in superior.columns if (superior[c] > limite).any()]
    return constantes + correlacionadas


# ------------------------------------------------------------------ 3. Transformação
def construir_preprocessamento(
    numericas: list[str],
    categoricas: list[str] | None = None,
    ordinais: dict[str, list[str]] | None = None,
) -> ColumnTransformer:
    """ColumnTransformer: imputa e padroniza as numéricas, codifica as categóricas e as ordinais.

    Tudo o que é *aprendido* com os dados (medianas, médias, desvios, categorias) fica aqui
    dentro, para ser ajustado só com os dados de treino e evitar fugas de informação.
    """
    categoricas = categoricas or []
    ordinais = ordinais or {}
    partes = [("num", Pipeline([("imputar", SimpleImputer(strategy="median", add_indicator=True)),
                                ("escalar", StandardScaler())]), numericas)]
    if categoricas:
        partes.append(("cat", Pipeline([("imputar", SimpleImputer(strategy="most_frequent")),
                                        ("codificar", OneHotEncoder(handle_unknown="ignore",
                                                                    sparse_output=False))]), categoricas))
    if ordinais:
        partes.append(("ord", Pipeline([("imputar", SimpleImputer(strategy="most_frequent")),
                                        ("codificar", OrdinalEncoder(categories=list(ordinais.values())))]),
                       list(ordinais)))
    return ColumnTransformer(partes, verbose_feature_names_out=False)


# ------------------------------------------------------------------ 5. Mineração
def comparar_modelos(
    modelos: dict[str, object],
    preprocessamento: ColumnTransformer,
    X: pd.DataFrame,
    y: pd.Series,
    metricas: tuple[str, ...] = ("roc_auc", "f1", "accuracy"),
    folds: int = 5,
    semente: int = 42,
) -> pd.DataFrame:
    """Validação cruzada estratificada de vários modelos, cada um num Pipeline com o pré-processamento."""
    cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=semente)
    linhas = {}
    for nome, modelo in modelos.items():
        pipe = Pipeline([("prep", clone(preprocessamento)), ("modelo", modelo)])
        r = cross_validate(pipe, X, y, cv=cv, scoring=list(metricas))
        linhas[nome] = {f"{m}_media": r[f"test_{m}"].mean() for m in metricas} | \
                       {f"{metricas[0]}_dp": r[f"test_{metricas[0]}"].std()}
    return pd.DataFrame(linhas).T.sort_values(f"{metricas[0]}_media", ascending=False).round(3)


# ------------------------------------------------------------------ 6. Avaliação
def lift_por_decil(y_real: pd.Series, probabilidade: np.ndarray) -> pd.DataFrame:
    """Ordena por probabilidade, divide em 10 grupos e compara a taxa real de cada um com a média.

    Um lift de 3 no 1.º decil quer dizer que, entre os 10 % com maior risco previsto,
    a taxa real é três vezes a taxa média: é aí que uma ação (por exemplo, de retenção) rende mais.
    """
    tabela = pd.DataFrame({"real": np.asarray(y_real), "prob": probabilidade})
    tabela["decil"] = pd.qcut(tabela["prob"].rank(method="first", ascending=False), 10, labels=range(1, 11))
    taxa_media = tabela["real"].mean()
    resumo = tabela.groupby("decil", observed=True).agg(casos=("real", "size"),
                                                        taxa_real=("real", "mean"),
                                                        prob_media=("prob", "mean"))
    resumo["lift"] = resumo["taxa_real"] / taxa_media
    return resumo.round(3)
