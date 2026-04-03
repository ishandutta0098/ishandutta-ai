from pydantic import BaseModel, Field
from datetime import datetime

class CompanyQuery(BaseModel):
    company: str = Field(..., description="Company name")
    ticker: str = Field("", description="Stock ticker symbol")

class FinancialMetrics(BaseModel):
    revenue: str = ""
    net_income: str = ""
    gross_margin: str = ""
    operating_margin: str = ""
    revenue_growth: str = ""
    market_cap: str = ""
    pe_ratio: str = ""

class CompetitorInfo(BaseModel):
    name: str
    market_cap: str = ""
    key_difference: str = ""

class AnalysisSection(BaseModel):
    trend_analysis: str = ""
    competitive_positioning: str = ""
    risks: list[str] = []
    catalysts: list[str] = []
    bull_case: str = ""
    bear_case: str = ""
    rating: str = "Hold"

class ResearchReport(BaseModel):
    company: str
    ticker: str
    generated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    executive_summary: str = ""
    full_report: str = ""
    rating: str = "Hold"
    metrics: FinancialMetrics = Field(default_factory=FinancialMetrics)
    competitors: list[CompetitorInfo] = []
    analysis: AnalysisSection = Field(default_factory=AnalysisSection)

class ReportResponse(BaseModel):
    company: str
    ticker: str
    report: str
    rating: str
    generated_at: str
    status: str = "completed"
    execution_log: list[str] = []
