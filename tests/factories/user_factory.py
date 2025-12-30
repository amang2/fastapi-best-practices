import factory
from factory import Faker
from uuid import uuid4

from src.user_profile.models import UserProfile

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserProfile
        sqlalchemy_session_persistence = "flush"

    id = factory.LazyFunction(uuid4)
    name = Faker("name")
    email = Faker("email")
    domain = Faker("domain_name")
    username = Faker("user_name")
    status = "active"
    is_deleted = False