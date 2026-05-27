from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.db.gender_migration import migrate_student_gender
from app.db.system_rbac_migration import migrate_system_rbac
from app.models.models import Student, User


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        migrate_student_gender(db)
        migrate_system_rbac(db)

        sample_students = [
            Student(name="张三", student_no="S001", gender="1", age=18, phone="13800138001", email="zhangsan@example.com", address="北京市朝阳区"),
            Student(name="李四", student_no="S002", gender="2", age=19, phone="13800138002", email="lisi@example.com", address="上海市浦东新区"),
            Student(name="王五", student_no="S003", gender="1", age=20, phone="13800138003", email="wangwu@example.com", address="广州市天河区"),
        ]
        for s in sample_students:
            existing = db.query(Student).filter(Student.student_no == s.student_no).first()
            if not existing:
                db.add(s)

        db.commit()
        print("数据库初始化完成!")
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
