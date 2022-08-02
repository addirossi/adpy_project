from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from models import *


class DB:
    def __init__(self, db_url) -> None:
        self.engine = sq.create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_db(self):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def add_user(self, vk_id, name, last_name):
        user = User(vk_id, name, last_name)
        self.session.add(user)
        self.session.commit()

    def add_search_params(self, user_id, country_id, city_id, sex, age_from, age_to):
        search_params = SearchParams(
            id=user_id, 
            country_id=country_id, 
            city_id=city_id,
            sex=sex,
            age_from=age_from,
            age_to=age_to 
            )
        self.session.add(search_params)
        self.session.commit()
    
    def add_user_match(self, user_id, match_vk_id, match_name, match_last_name, match_profile_url):
        match_result = SearchResult(
            user_id=user_id, 
            vk_id=match_vk_id, 
            name=match_name,
            last_name=match_last_name,
            profile_link=match_profile_url
            )
        self.session.add(match_result)
        self.session.commit()
    
    def add_match_photo(self, owner_id, photos_urls_list):
        photos = []
        for url in photos_urls_list:
            obj = Photo(url=url, owner_id=owner_id)
            photos.append(obj)
        self.session.add_all(photos)
        self.session.commit()

    def like_user(self, user_id, match_id):
        self.session.query(SearchResult).filter(SearchResult.user_id == user_id, SearchResult.vk_id == match_id).update(is_favorite=True)
    
    def blacklist_user(self, user_id, match_id):
        self.session.query(SearchResult).filter(SearchResult.user_id == user_id, SearchResult.vk_id == match_id).update(blacklisted=True)

    def get_favorites_list(self, user_id):
        return self.session.query(SearchResult).filter(SearchResult.user_id == user_id, SearchResult.is_favorite==True).all()

    def get_blacklist(self, user_id):
        return self.session.query(SearchResult).filter(SearchResult.user_id == user_id, SearchResult.blacklisted == True).all()
