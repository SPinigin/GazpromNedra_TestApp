from pydantic import BaseModel


class OrgBase(BaseModel):
    name: str


class OrgCreate(OrgBase):
    pass


class Company(OrgBase):
    id: int

    class Config:
        from_attributes = True


class LicenseStatusBase(BaseModel):
    name: str


class LicenseStatusCreate(LicenseStatusBase):
    pass


class LicenseStatus(LicenseStatusBase):
    id: int

    class Config:
        from_attributes = True


class WellStatusBase(BaseModel):
    name: str


class WellStatusCreate(WellStatusBase):
    pass


class WellStatus(WellStatusBase):
    id: int

    class Config:
        from_attributes = True