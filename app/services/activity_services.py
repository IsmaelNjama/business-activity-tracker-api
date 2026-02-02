from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException
from datetime import datetime
import uuid

from app.models.activity import Activity
from app.schemas.activities import (
    ActivityCreate,
    ActivityUpdate,
    ActivityFilters,
    ExpenseActivityCreate,
    SalesActivityCreate,
    CustomerActivityCreate,
    ProductionActivityCreate,
    StorageActivityCreate
)


class ActivityServices:

    @staticmethod
    def create_activity(
        db: Session,
        activity_data: ActivityCreate,
        user_id: str
    ) -> Activity:
        """Create a new activity"""
        now = datetime.utcnow()

        # Create base activity with common fields
        activity_dict = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "type": activity_data.type,
            "created_at": now,
            "updated_at": now
        }

        # Add type-specific fields
        if activity_data.type == "expense":
            activity_dict.update({
                "receipt_image": activity_data.receipt_image,
                "description": activity_data.description
            })

        elif activity_data.type == "sales":
            activity_dict.update({
                "receipt_image": activity_data.receipt_image,
                "date": activity_data.date,
                "time": activity_data.time,
                "serving_employee": activity_data.serving_employee,
                "buyer_name": activity_data.buyer_name
            })

        elif activity_data.type == "customer":
            activity_dict.update({
                "customer_name": activity_data.customer_name,
                "service_date": activity_data.service_date,
                "service_type": activity_data.service_type,
                "notes": activity_data.notes
            })

        elif activity_data.type == "production":
            activity_dict.update({
                "raw_material_weight": activity_data.raw_material_weight,
                "weight_unit": activity_data.weight_unit,
                "machine_image_before": activity_data.machine_image_before,
                "machine_image_after": activity_data.machine_image_after,
                "notes": activity_data.notes
            })

        elif activity_data.type == "storage":
            activity_dict.update({
                "location": activity_data.location,
                "item_description": activity_data.item_description,
                "quantity": activity_data.quantity,
                "condition": activity_data.condition
            })

        db_activity = Activity(**activity_dict)

        try:
            db.add(db_activity)
            db.commit()
            db.refresh(db_activity)
            return db_activity
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Failed to create activity"
            )

    @staticmethod
    def get_all_activities(db: Session) -> List[Activity]:
        """Get all activities"""
        return db.query(Activity).order_by(Activity.created_at.desc()).all()

    @staticmethod
    def get_activity_by_id(db: Session, activity_id: str) -> Optional[Activity]:
        """Get activity by ID"""
        return db.query(Activity).filter(Activity.id == activity_id).first()

    @staticmethod
    def get_activities_by_user_id(db: Session, user_id: str) -> List[Activity]:
        """Get all activities for a specific user"""
        return db.query(Activity).filter(
            Activity.user_id == user_id
        ).order_by(Activity.created_at.desc()).all()

    @staticmethod
    def get_activities_by_type(db: Session, activity_type: str) -> List[Activity]:
        """Get all activities of a specific type"""
        return db.query(Activity).filter(
            Activity.type == activity_type
        ).order_by(Activity.created_at.desc()).all()

    @staticmethod
    def get_activities_by_user_and_type(
        db: Session,
        user_id: str,
        activity_type: str
    ) -> List[Activity]:
        """Get activities for a user filtered by type"""
        return db.query(Activity).filter(
            Activity.user_id == user_id,
            Activity.type == activity_type
        ).order_by(Activity.created_at.desc()).all()

    @staticmethod
    def filter_activities(db: Session, filters: ActivityFilters) -> List[Activity]:
        """Filter activities based on multiple criteria"""
        query = db.query(Activity)

        # Filter by user ID
        if filters.user_id:
            query = query.filter(Activity.user_id == filters.user_id)

        # Filter by type
        if filters.type:
            query = query.filter(Activity.type == filters.type)

        # Filter by date range
        if filters.start_date:
            start_date = datetime.fromisoformat(filters.start_date)
            query = query.filter(Activity.created_at >= start_date)

        if filters.end_date:
            end_date = datetime.fromisoformat(filters.end_date)
            # Set to end of day
            end_date = end_date.replace(
                hour=23, minute=59, second=59, microsecond=999999)
            query = query.filter(Activity.created_at <= end_date)

        return query.order_by(Activity.created_at.desc()).all()

    @staticmethod
    def get_recent_activities(
        db: Session,
        user_id: str,
        limit: int = 10
    ) -> List[Activity]:
        """Get recent activities for a user"""
        return db.query(Activity).filter(
            Activity.user_id == user_id
        ).order_by(Activity.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_all_recent_activities(db: Session, limit: int = 10) -> List[Activity]:
        """Get recent activities for all users (admin view)"""
        return db.query(Activity).order_by(
            Activity.created_at.desc()
        ).limit(limit).all()

    @staticmethod
    def get_activity_counts_by_type(db: Session, user_id: str) -> dict:
        """Get activity counts by type for a user"""
        activities = ActivityServices.get_activities_by_user_id(db, user_id)

        counts = {
            "expense": 0,
            "sales": 0,
            "customer": 0,
            "production": 0,
            "storage": 0
        }

        for activity in activities:
            counts[activity.type] += 1

        return counts

    @staticmethod
    def get_all_activity_counts_by_type(db: Session) -> dict:
        """Get activity counts by type for all users (admin view)"""
        activities = db.query(Activity).all()

        counts = {
            "expense": 0,
            "sales": 0,
            "customer": 0,
            "production": 0,
            "storage": 0
        }

        for activity in activities:
            counts[activity.type] += 1

        return counts

    @staticmethod
    def update_activity(
        db: Session,
        activity_id: str,
        activity_update: ActivityUpdate
    ) -> Activity:
        """Update an existing activity"""
        activity = ActivityServices.get_activity_by_id(db, activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        # Get update data, excluding unset fields
        activity_update_data = activity_update.model_dump(
            exclude_unset=True,
            by_alias=False
        )

        # Update the timestamp
        activity_update_data["updated_at"] = datetime.utcnow()

        # Apply updates
        for field, value in activity_update_data.items():
            setattr(activity, field, value)

        try:
            db.add(activity)
            db.commit()
            db.refresh(activity)
            return activity
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Failed to update activity"
            )

    @staticmethod
    def delete_activity(db: Session, activity_id: str) -> bool:
        """Delete an activity"""
        activity = ActivityServices.get_activity_by_id(db, activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        try:
            db.delete(activity)
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

    @staticmethod
    def get_activities_grouped_by_date(
        db: Session,
        user_id: Optional[str] = None
    ) -> dict:
        """Get activities grouped by date"""
        if user_id:
            activities = ActivityServices.get_activities_by_user_id(
                db, user_id)
        else:
            activities = ActivityServices.get_all_activities(db)

        grouped = {}
        for activity in activities:
            date_key = activity.created_at.date().isoformat()
            if date_key not in grouped:
                grouped[date_key] = []
            grouped[date_key].append(activity)

        return grouped

    @staticmethod
    def get_activity_stats(
        db: Session,
        user_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> dict:
        """Get activity statistics for a date range"""
        filters = ActivityFilters(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )

        activities = ActivityServices.filter_activities(db, filters)
        counts = ActivityServices.get_activity_counts_by_type(db, user_id)

        return {
            "total": len(activities),
            "by_type": counts,
            "activities": activities
        }
