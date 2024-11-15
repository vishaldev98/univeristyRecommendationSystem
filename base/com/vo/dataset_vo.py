from base import db


class DatasetVO(db.Model):
    __tablename__ = 'dataset_table'
    dataset_id = db.Column('dataset_id', db.Integer, primary_key=True, autoincrement=True)
    dataset_file_name = db.Column('dataset_file_name', db.String(100), nullable=False)
    dataset_file_path = db.Column('dataset_file_path', db.String(100), nullable=False)
    dataset_datetime = db.Column('dataset_datetime', db.DateTime, nullable=False)
    dataset_description = db.Column('dataset_description', db.String(100), nullable=False)

    def as_dict(self):
        return {
            'dataset_id': self.dataset_id,
            'dataset_file_name': self.dataset_file_name,
            'dataset_file_path': self.dataset_file_path,
            'dataset_datetime': self.dataset_datetime,
            'dataset_description': self.dataset_description
        }


