"""This module contains functions for the ELT process."""

from src.control.ingestion_control import get_last_date_ingestion, update_date_ingestion
from src.ingestion.postgres_extractor import extract_data_postgres
from src.loaders.snowflake_load import load_incremental_data

__all__ = ["get_last_date_ingestion", "update_date_ingestion", "extract_data_postgres", "load_incremental_data"]