from ..meta_classes import DataSetProperties
from ..classes import Product, ProductID, Person, PersonID, PersonMetaProperties, IsGoldenFlag, ProductStyleEnum, PersonStylePreferenceEnum
from ..utils import choose_weighted_option
from typing import Set
import random


class SimpleDataSet(object):
    def __init__(self, properties: DataSetProperties, opinion_function):
        self.opinion_function = opinion_function
        self.properties = properties
        self._public_product_ids: Set[ProductID] = set()
        self._public_people_ids: Set[PersonID] = set()

        self.init_enums()

    @staticmethod
    def init_enums():
        ProductStyleEnum.LIKES_A: ProductStyleEnum()
        ProductStyleEnum.LIKES_B: ProductStyleEnum()

        PersonStylePreferenceEnum.A: PersonStylePreferenceEnum()
        PersonStylePreferenceEnum.B: PersonStylePreferenceEnum()

    def generate_public_products(self):
        for i in range(self.properties.n_products):
            style = choose_weighted_option(self.properties.product_styles_distribution)
            product = Product(ProductID.new_random(), IsGoldenFlag(False), style)
            self._public_product_ids.add(product.id)
            yield product

    def generate_public_people(self):
        for i in range(self.properties.n_people):
            number_of_reviews = choose_weighted_option(self.properties.reviews_per_person_distribution)
            meta = PersonMetaProperties(number_of_reviews=number_of_reviews)
            style_preference = choose_weighted_option(self.properties.person_styles_distribution)
            person = Person(PersonID.new_random(), IsGoldenFlag(False), style_preference, meta_properties=meta)
            self._public_people_ids.add(person.id)
            yield person

    def generate_reviews(self, person: Person, product: Product) -> float:
        for i in range(person.meta_properties.number_of_reviews):
            self.opinion_function(person, product)

    def pick_public_product(self) -> ProductID:
        return random.choice(self._public_product_ids)

    def pick_public_person(self) -> PersonID:
        return random.choice(self._public_people_ids)