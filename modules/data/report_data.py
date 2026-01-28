from dataclasses import dataclass, field
import pandas as pd

from .assignment_data import SplitManager
from .receipt_data import ItemData


@dataclass
class ParticipantReportData:
    """Report data for a single participant."""

    name: str
    items: list[ItemData]
    purchased_subtotal: float
    purchased_others: float
    purchased_total: float

    def to_dataframe_display(self) -> pd.DataFrame:
        """Convert to dataframe for display."""
        data = [
            {
                "Item": item.name,
                "Price": item.total_price,
            }
            for item in self.items
        ]
        return pd.DataFrame(data)


@dataclass
class ReportData:
    """Class that contains the final report data."""

    participants_reports: list[ParticipantReportData]

    @classmethod
    def from_split_manager(cls, manager: SplitManager) -> "ReportData":
        """Create report from split manager.

        Args:
            manager (SplitManager): the split manager

        Returns:
            ReportData: the report data
        """
        receipt_total = manager.receipt_data.total
        receipt_subtotal = manager.receipt_data.subtotal
        others_total = receipt_total - receipt_subtotal

        participants_reports = []
        for participant in manager.get_all_participants():
            assignments = manager.get_participant_items_assignment_list(participant.id)
            
            # Reconstruct items list specifically for this participant
            param_items = [
                ItemData(
                    name=a.item.name,
                    count=a.assigned_count,
                    total_price=a.item.unit_price * a.assigned_count
                )
                for a in assignments
            ]

            # Calculate subtotal for this participant
            participant_subtotal = sum(item.total_price for item in param_items)
            
            # Proportional distribution of others
            ratio = 0
            if receipt_subtotal > 0:
                ratio = participant_subtotal / receipt_subtotal
                
            participant_others = others_total * ratio
            participant_total = participant_subtotal + participant_others

            participants_reports.append(
                ParticipantReportData(
                    name=participant.name,
                    items=param_items,
                    purchased_subtotal=participant_subtotal,
                    purchased_others=participant_others,
                    purchased_total=participant_total,
                )
            )


        return cls(participants_reports=participants_reports)
