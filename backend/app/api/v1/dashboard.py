from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from decimal import Decimal
from app.services.cache import get_revenue_summary
from app.core.auth import authenticate_request as get_current_user

router = APIRouter()

@router.get("/dashboard/summary")
async def get_dashboard_summary(
    property_id: str,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    tenant_id = getattr(current_user, "tenant_id", "default_tenant") or "default_tenant"
    revenue_data = await get_revenue_summary(property_id, tenant_id)

    # total_revenue_float = float(revenue_data['total'])  # ❌ THIS IS THE BUG
    
    # FIX: Keep Decimal precision, convert to string for JSON serialization
    total_revenue = revenue_data['total']
    if isinstance(total_revenue, Decimal):
        total_revenue_str = str(total_revenue)
    else:
        total_revenue_str = str(Decimal(str(total_revenue)))
    
    return {
        "property_id": revenue_data['property_id'],
        "total_revenue": total_revenue_str,  # ✅ Preserve precision
        "currency": revenue_data['currency'],
        "reservations_count": revenue_data['count']
    }