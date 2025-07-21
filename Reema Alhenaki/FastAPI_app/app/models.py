from typing import Optional
from sqlalchemy import Column, Date, DateTime, Double, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, Table, Text, Time
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime



class HISPatient(Base):
    __tablename__ = 'HIS_Patient'
    __table_args__ = (
        PrimaryKeyConstraint('PatientID', name='HIS_Patient_pkey'),
    )

    PatientID: Mapped[int] = mapped_column(Integer, primary_key=True)
    RegistrationDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    FirstName: Mapped[str] = mapped_column(String(150))
    MiddleName: Mapped[str] = mapped_column(String(150))
    LastName: Mapped[str] = mapped_column(String(150))
    Gender: Mapped[int] = mapped_column(Integer)
    DateofBirth: Mapped[datetime.datetime] = mapped_column(DateTime)
    NationalityID: Mapped[str] = mapped_column(String(3))
    FirstVisit: Mapped[datetime.datetime] = mapped_column(DateTime)
    LastVisit: Mapped[datetime.datetime] = mapped_column(DateTime)
    NoOfVisit: Mapped[int] = mapped_column(Integer)
    MobileNumber: Mapped[int] = mapped_column(Integer)
    EmailAddress: Mapped[Optional[str]] = mapped_column(String(150))
    IsPregnant: Mapped[Optional[int]] = mapped_column(Integer)
    BloodGroup: Mapped[Optional[int]] = mapped_column(Integer)
    RHFactor: Mapped[Optional[str]] = mapped_column(String(10))
    RegisteredDoctor: Mapped[Optional[int]] = mapped_column(Integer)
    EmergencyContactName: Mapped[Optional[str]] = mapped_column(String(150))
    EmergencyContactNo: Mapped[Optional[int]] = mapped_column(Integer)


t_HIS_Appointment = Table(
    'HIS_Appointment', Base.metadata,
    Column('AppointmentNo', Integer, nullable=False),
    Column('AppointmentDate', DateTime),
    Column('PatientID', Integer, nullable=False),
    Column('ClinicID', Integer, nullable=False),
    Column('DoctorID', Integer, nullable=False),
    Column('StartTime', DateTime, nullable=False),
    Column('EndTime', DateTime, nullable=False),
    Column('VisitType', Integer, nullable=False),
    Column('VisitFor', Integer, nullable=False),
    Column('Notes', String(150)),
    Column('IsVirtual', Integer),
    ForeignKeyConstraint(['PatientID'], ['HIS_Patient.PatientID'], name='HIS_Appointment_PatientID_fkey')
)


t_HIS_DoctorOrder = Table(
    'HIS_DoctorOrder', Base.metadata,
    Column('PatientID', Integer, nullable=False),
    Column('ActualOrderDate', Date, nullable=False),
    Column('ActualOrderTime', Time),
    Column('OrderNotes', Text),
    Column('NursingNotes', Text),
    ForeignKeyConstraint(['PatientID'], ['HIS_Patient.PatientID'], name='HIS_DoctorOrder_PatientID_fkey')
)


t_HIS_PatientVitalSigns = Table(
    'HIS_PatientVitalSigns', Base.metadata,
    Column('PatientID', Integer, nullable=False),
    Column('WeightKg', Double(53)),
    Column('HeightCm', Double(53)),
    Column('BodyMassIndex', Double(53)),
    Column('TemperatureCelcius', Double(53)),
    Column('PulseBeatPerMinute', Integer),
    Column('RespirationBeatPerMinute', Integer),
    Column('BloodPressureLower', Integer),
    Column('BloodPressureHigher', Integer),
    Column('SAO2', Integer),
    Column('FIO2', Double(53)),
    Column('PainScore', Double(53)),
    Column('PainLocation', String(40)),
    Column('PainDuration', String(40)),
    Column('PainCharacter', String(40)),
    Column('PainFrequency', String(40)),
    Column('TriageCategory', Integer),
    Column('GCScore', Double(53)),
    Column('CreatedOn', DateTime),
    ForeignKeyConstraint(['PatientID'], ['HIS_Patient.PatientID'], name='HIS_PatientVitalSigns_PatientID_fkey')
)
