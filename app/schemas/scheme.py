from enum import StrEnum
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
import datetime 


class FundFamily(StrEnum):
    FUND_360_ONE = "360 ONE Mutual Fund (Formerly Known as IIFL Mutual Fund)"
    ADITYA_BIRLA_SUN_LIFE = "Aditya Birla Sun Life Mutual Fund"
    ANGEL_ONE = "Angel One Mutual Fund"
    AXIS = "Axis Mutual Fund"
    BAJAJ_FINSERV = "Bajaj Finserv Mutual Fund"
    BANDHAN = "Bandhan Mutual Fund"
    BANK_OF_INDIA = "Bank of India Mutual Fund"
    BARODA_BNP_PARIBAS = "Baroda BNP Paribas Mutual Fund"
    CANARA_ROBECO = "Canara Robeco Mutual Fund"
    DSP = "DSP Mutual Fund"
    EDELWEISS = "Edelweiss Mutual Fund"
    FRANKLIN_TEMPLETON = "Franklin Templeton Mutual Fund"
    GROWW = "Groww Mutual Fund"
    HDFC = "HDFC Mutual Fund"
    HSBC = "HSBC Mutual Fund"
    HELIOS = "Helios Mutual Fund"
    ICICI_PRUDENTIAL = "ICICI Prudential Mutual Fund"
    ITI = "ITI Mutual Fund"
    INVESCO = "Invesco Mutual Fund"
    JM_FINANCIAL = "JM Financial Mutual Fund"
    KOTAK_MAHINDRA = "Kotak Mahindra Mutual Fund"
    LIC = "LIC Mutual Fund"
    MAHINDRA_MANULIFE = "Mahindra Manulife Mutual Fund"
    MIRAE_ASSET = "Mirae Asset Mutual Fund"
    MOTILAL_OSWAL = "Motilal Oswal Mutual Fund"
    NJ = "NJ Mutual Fund"
    NAVI = "Navi Mutual Fund"
    NIPPON_INDIA = "Nippon India Mutual Fund"
    OLD_BRIDGE = "Old Bridge Mutual Fund"
    PGIM_INDIA = "PGIM India Mutual Fund"
    PPFAS = "PPFAS Mutual Fund"
    QUANTUM = "Quantum Mutual Fund"
    SBI = "SBI Mutual Fund"
    SAMCO = "Samco Mutual Fund"
    SHRIRAM = "Shriram Mutual Fund"
    SUNDARAM = "Sundaram Mutual Fund"
    TATA = "Tata Mutual Fund"
    TAURUS = "Taurus Mutual Fund"
    TRUST = "Trust Mutual Fund"
    UTI = "UTI Mutual Fund"
    UNIFI = "Unifi Mutual Fund"
    UNION = "Union Mutual Fund"
    WHITE_OAK_CAPITAL = "WhiteOak Capital Mutual Fund"
    ZERODHA = "Zerodha Mutual Fund"
    QUANT = "quant Mutual Fund"


class SchemeType(StrEnum):
    open = 'Open Ended Schemes'



class SchemeQuery(BaseModel):
    mutual_fund_family: FundFamily
    scheme_type: SchemeType
    page: int = Field(default=1, ge=1, description="Page number starting from 1")
    page_size: int = Field(default=10, ge=1, le=100, description="Number of items per page (max 100)")

    model_config = ConfigDict(
        from_attributes=True
    )

class SchemeBase(BaseModel):
    scheme_code: int
    isin_div_payout_isin_growth: str
    isin_div_reinvestment: str
    scheme_name: str
    net_asset_value: float
    start_date: datetime.date
    scheme_type: SchemeType
    scheme_category: str
    mutual_fund_family: FundFamily
    
    model_config = ConfigDict(
        from_attributes=True
    )



class SchemeCreate(SchemeBase): 
    pass

class SchemeResponseFull(SchemeBase):
    pass


class SchemeResponseBasic(BaseModel):
    scheme_code: int
    scheme_name: str
    mutual_fund_family: FundFamily
    
    model_config = ConfigDict(
        from_attributes=True
    )



class SchemeResultSet(BaseModel):
    data: list[SchemeResponseBasic]
    total: int



class LatestSchemeResponse(BaseModel):
    scheme_code: int = Field(..., alias="Scheme_Code")
    isin_div_payout_isin_growth: str = Field(..., alias="ISIN_Div_Payout_ISIN_Growth")
    isin_div_reinvestment: str = Field(..., alias="ISIN_Div_Reinvestment")
    scheme_name: str = Field(..., alias="Scheme_Name")
    net_asset_value: float = Field(..., alias="Net_Asset_Value")
    scheme_type: str = Field(..., alias="Scheme_Type")
    scheme_category: str = Field(..., alias="Scheme_Category")
    mutual_fund_family: str = Field(..., alias="Mutual_Fund_Family")  # Assuming FundFamily is str here
    start_date_str: str = Field(..., alias="Date")
    start_date: datetime.date | None = None

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @model_validator(mode="after")
    def set_start_date(self) -> "LatestSchemeResponse":
        if self.start_date_str:
            self.start_date = datetime.datetime.strptime(self.start_date_str, "%d-%b-%Y").date()
        return self
