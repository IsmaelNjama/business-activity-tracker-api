from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.activities import (
    ActivityCreate,
    ActivityOut,
    ActivityUpdate,
    ActivityFilters
)
from app.services.activity_services import ActivityServices
from app.utils.auth import get_current_user


router = APIRouter(prefix="/v1/activities", tags=["activities"])


@router.post("", response_model=ActivityOut, status_code=201)
async def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Create a new activity.
    The activity type determines which fields are required.
    """
    return ActivityServices.create_activity(
        db=db,
        activity_data=activity,
        user_id=current_user.id
    )


@router.get("", response_model=List[ActivityOut])
async def get_activities(
    user_id: Optional[str] = Query(None, alias="userId"),
    type: Optional[str] = None,
    start_date: Optional[str] = Query(None, alias="startDate"),
    end_date: Optional[str] = Query(None, alias="endDate"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get activities with optional filters.
    Regular users can only see their own activities.
    Admins can see all activities or filter by userId.
    """
    # If not admin and trying to access other user's data
    if not current_user.is_admin and user_id and user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # If regular user, force filter by their own user_id
    if not current_user.is_admin:
        user_id = current_user.id

    # If no filters, return all (filtered by user if not admin)
    if not any([user_id, type, start_date, end_date]):
        if user_id:
            return ActivityServices.get_activities_by_user_id(db, user_id)
        return ActivityServices.get_all_activities(db)

    # Apply filters
    filters = ActivityFilters(
        user_id=user_id,
        type=type,
        start_date=start_date,
        end_date=end_date
    )
    return ActivityServices.filter_activities(db, filters)


@router.get("/me", response_model=List[ActivityOut])
async def get_my_activities(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get all activities for the current user"""
    return ActivityServices.get_activities_by_user_id(db, current_user.id)


@router.get("/me/recent", response_model=List[ActivityOut])
async def get_my_recent_activities(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get recent activities for the current user"""
    return ActivityServices.get_recent_activities(db, current_user.id, limit)


@router.get("/me/stats")
async def get_my_activity_stats(
    start_date: Optional[str] = Query(None, alias="startDate"),
    end_date: Optional[str] = Query(None, alias="endDate"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get activity statistics for the current user"""
    return ActivityServices.get_activity_stats(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/me/counts")
async def get_my_activity_counts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get activity counts by type for the current user"""
    return ActivityServices.get_activity_counts_by_type(db, current_user.id)


@router.get("/me/type/{activity_type}", response_model=List[ActivityOut])
async def get_my_activities_by_type(
    activity_type: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get activities of a specific type for the current user"""
    valid_types = ["expense", "sales", "customer", "production", "storage"]
    if activity_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid activity type. Must be one of: {', '.join(valid_types)}"
        )

    return ActivityServices.get_activities_by_user_and_type(
        db=db,
        user_id=current_user.id,
        activity_type=activity_type
    )


@router.get("/me/grouped-by-date")
async def get_my_activities_grouped_by_date(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get activities grouped by date for the current user"""
    return ActivityServices.get_activities_grouped_by_date(db, current_user.id)


@router.get("/{activity_id}", response_model=ActivityOut)
async def get_activity(
    activity_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get a specific activity by ID"""
    activity = ActivityServices.get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check authorization
    if not current_user.is_admin and activity.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return activity


@router.patch("/{activity_id}", response_model=ActivityOut)
async def update_activity(
    activity_id: str,
    activity_update: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Update an activity"""
    activity = ActivityServices.get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check authorization
    if not current_user.is_admin and activity.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return ActivityServices.update_activity(db, activity_id, activity_update)


@router.delete("/{activity_id}", status_code=204)
async def delete_activity(
    activity_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Delete an activity"""
    activity = ActivityServices.get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check authorization
    if not current_user.is_admin and activity.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    success = ActivityServices.delete_activity(db, activity_id)
    if not success:
        raise HTTPException(
            status_code=500, detail="Failed to delete activity")

    return None


# Admin-only endpoints
@router.get("/admin/all", response_model=List[ActivityOut])
async def admin_get_all_activities(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Admin: Get all activities from all users"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    return ActivityServices.get_all_activities(db)


@router.get("/admin/recent", response_model=List[ActivityOut])
async def admin_get_recent_activities(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Admin: Get recent activities from all users"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    return ActivityServices.get_all_recent_activities(db, limit)


@router.get("/admin/counts")
async def admin_get_activity_counts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Admin: Get activity counts by type for all users"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    return ActivityServices.get_all_activity_counts_by_type(db)


@router.get("/admin/grouped-by-date")
async def admin_get_activities_grouped_by_date(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Admin: Get all activities grouped by date"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    return ActivityServices.get_activities_grouped_by_date(db)
