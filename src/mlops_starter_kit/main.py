# src/mlops_starter_kit/main.py

import logging
from pathlib import Path

from mlops_starter_kit.config import get_config_and_logger
from mlops_starter_kit.utils import (
    load_data,
    split_data,
    train_model,
    evaluate_model,
    save_model,
)

def main():
    # Load configuration and initialize logging
    cfg = get_config_and_logger()
    logger = logging.getLogger(__name__)
    logger.info(f"Starting project: {cfg.project.name}")

    # 1) Load raw data
    data_path = Path(cfg.dataset.path) / cfg.dataset.filename
    logger.info(f"Loading data from {data_path}")
    df = load_data(data_path)

    # 2) Split into train/test
    logger.info("Splitting data into train and test sets")
    X_train, X_test, y_train, y_test = split_data(
        df,
        target_col=cfg.dataset.target_col,
        test_size=cfg.dataset.test_size,
        random_state=cfg.dataset.random_seed,
    )

    # 3) Train the model
    logger.info(f"Training model {cfg.model.name} with params {cfg.model.params}")
    model = train_model(
        X_train,
        y_train,
        model_name=cfg.model.name,
        **cfg.model.params,
    )

    # 4) Evaluate
    logger.info("Evaluating model performance on test set")
    metrics = evaluate_model(model, X_test, y_test)
    for k, v in metrics.items():
        logger.info(f"  {k}: {v:.4f}")

    # 5) Save trained artifact
    save_dir = Path(cfg.model.artifact_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    model_path = save_dir / f"{cfg.model.name}.pkl"
    save_model(model, model_path)
    logger.info(f"Model saved to {model_path}")

    logger.info("Pipeline complete.")

if __name__ == "__main__":
    main()

