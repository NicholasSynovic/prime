"""
Type classes.

Copyright (C) 2025 Nicholas M. Synovic.

"""

from pandas import DataFrame, Series
from pydantic import BaseModel, ValidationError


def validate_df(model: type[BaseModel], df: DataFrame) -> None:
    """
    Validate each row in a DataFrame against a Pydantic model.

    Args:
        model (type[BaseModel]): The Pydantic model class to validate against.
        df (DataFrame): The DataFrame to validate.

    """

    def _run(data: Series) -> None:
        """
        Instantiate a Pydantic model from a Pandas Series row.

        Converts the Series to a dictionary and validates it using the Pydantic model.
        Raises a ValidationError if the data does not conform to the model schema.

        Args:
            data (Series): A row from a DataFrame containing fields matching the
                Pydantic model.

        """
        row: dict = data.to_dict()
        try:
            model(**row)
        except ValidationError as ve:
            raise ve

    df.apply(_run, axis=1)
