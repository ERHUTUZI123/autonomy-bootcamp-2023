"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
    """

    def __init__(
        self,
        waypoint: location.Location,
        acceptance_radius: float,
    ) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        self.has_sent_landing_command = False

    def if_reach(
        self, des: location.Location, ob: location.Location, acceptance_radius: float
    ) -> bool:
        """
        Check if the object is within the acceptance radius of the destination.
        """
        dx = des.location_x
        dy = des.location_y
        ox = ob.location_x
        oy = ob.location_y

        if ((dx - ox) ** 2 <= acceptance_radius**2) and ((dy - oy) ** 2 <= acceptance_radius**2):
            return True
        return False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self,
        report: drone_report.DroneReport,
        landing_pad_locations: "list[location.Location]",
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        if report.status == drone_status.DroneStatus.HALTED and self.command_index < 1:
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x,
                self.waypoint.location_y,
            )
            self.command_index += 1

        elif (
            report.status == drone_status.DroneStatus.HALTED
            and not self.has_sent_landing_command
            and self.if_reach(report.position, self.waypoint, self.acceptance_radius)
        ):
            command = commands.Command.create_land_command()
            self.has_sent_landing_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
