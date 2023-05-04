
"""This file some pipeline to preprocess the data"""

#  MANAGEMENT ENVIRONMENT --------------------------------
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from .import_data import import_yaml_config, import_data


def pipeline_fit_transform_data_bank() -> Pipeline:

    config = import_yaml_config()
    path_train_data = config["path"]["bank_dataset_path"]
    df = import_data(path_train_data)

    test_fraction = config["model"]["test_fraction"]

    train, _ = train_test_split(
        df, test_size=test_fraction, stratify=df["deposit"], random_state=42
    )

    train = train.drop("deposit", axis="columns")

    # Sélectionner les colonnes de type "object"
    colonnes_object = train.select_dtypes(include=["object"]).columns.tolist()

    # Sélectionner les colonnes de type "int"
    colonnes_int = train.select_dtypes(include=["int"]).columns.tolist()

    numeric_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="mean")),
               ("scaler", MinMaxScaler())
               ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent",
                                      fill_value="missing")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, colonnes_int),
            ("cat", categorical_transformer, colonnes_object),
        ],
        remainder="passthrough",
    )

    preprocessing_pipeline = Pipeline([("preprocessor", preprocessor)])

    preprocessing_pipeline.fit_transform(train)

    return preprocessing_pipeline


def pipeline_ml_train_bank(df, ML_Model) -> Pipeline:

    # Sélectionner les colonnes de type "object"
    colonnes_object = df.select_dtypes(include=["object"]).columns.tolist()

    # Sélectionner les colonnes de type "int"
    colonnes_int = df.select_dtypes(include=["int"]).columns.tolist()

    numeric_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="mean")),
               ("scaler", MinMaxScaler())
               ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent",
                                      fill_value="missing")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, colonnes_int),
            ("cat", categorical_transformer, colonnes_object),
        ],
        remainder="passthrough",
    )

    pipeline_ml = Pipeline(
        [("preprocessor", preprocessor),
         ("classifier", ML_Model)
         ]
    )

    return pipeline_ml