from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import relationship,backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = "courses"

    index = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    units = Column(String)
    description  = Column(String)
    timeperweek = Column(String)
    prereqs = Column(String)
    subject = Column(String)
    courselevel = Column(String)
    grading = Column(String)
    finals = Column(String)
    restrictions = Column(String)

    def __init__(self, name="",code="",units="",description="",timeperweek="",prereqs="",subject="",courselevel="",grading="",finals="",restrictions=""):
        self.name = name
        self.code = code
        self.units = units
        self.description = description
        self.timeperweek = timeperweek
        self.prereqs = prereqs
        self.subject =subject
        self.courselevel = courselevel
        self.grading = grading
        self.finals = finals
        self.restrictions = restrictions

    def __repr__(self):
        return "Course<%s>"%self.code

    def to_dict(self):
        d = dict()
        d['name'] = self.name
        return d

if __name__ == "__main__":
    engine = create_engine('sqlite:///courses.db', echo=False)
    Base.metadata.create_all(engine)
    print("Created Database")
