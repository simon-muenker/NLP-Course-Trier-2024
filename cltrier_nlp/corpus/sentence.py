import typing

import pandas
import pydantic

from .. import functional


class Sentence(pydantic.BaseModel):
    content: str

    language: str = None
    tokens: typing.List[str] = pydantic.Field(default_factory=lambda: [])

    def model_post_init(self, __context) -> None:

        self.content = self.content.replace("\n", " ")

        if not self.language:
            self.language = functional.text.detect_language(self.content)

        if not self.tokens:
            self.tokens = functional.text.tokenize(self.content)

    @pydantic.computed_field
    @property
    def bigrams(self) -> typing.List[typing.Tuple[str, ...]]:
        return functional.text.ngrams(self.tokens, 2)

    @pydantic.computed_field
    @property
    def trigrams(self) -> typing.List[typing.Tuple[str, ...]]:
        return functional.text.ngrams(self.tokens, 3)

    @pydantic.computed_field
    @property
    def tetragram(self) -> typing.List[typing.Tuple[str, ...]]:
        return functional.text.ngrams(self.tokens, 4)

    @pydantic.computed_field
    @property
    def pentagram(self) -> typing.List[typing.Tuple[str, ...]]:
        return functional.text.ngrams(self.tokens, 5)

    def to_row(self) -> pandas.Series:
        return pandas.Series(self.model_dump())

    def __len__(self) -> int:
        return len(self.tokens)
