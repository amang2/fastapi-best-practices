
import pytest
from sqlalchemy import select
from src.user_profile.models import UserProfile

@pytest.mark.asyncio
class TestUserApi:

    async def test_create_user(self,async_client,db_session):
        """
        Test creating a new user via API.
        """
        # Build test user data (not persisted yet)
        user_data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "domain": "example.com",
            "username": "testuser",
            "status": "active"
        }

        # Call API to create user
        response = await async_client.post(
        "/user/create",
        json=user_data)
        assert response.status_code == 201
        data = response.json()
        columns_to_select = data.keys()
        columns = [getattr(UserProfile, col) for col in columns_to_select]
        query = select(*columns).where(UserProfile.email == user_data["email"])
        result = await db_session.execute(query)
        row = result.first()
        if row:
            user_data_dict = dict(zip(columns_to_select, row))
            assert user_data_dict["email"] == user_data["email"]
            assert user_data_dict["name"] == user_data["name"]
            assert "id" in user_data_dict
        