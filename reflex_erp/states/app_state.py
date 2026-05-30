import reflex as rx
from typing import TypedDict
#from faker import Faker
from reflex_erp.db import collection

# Setup faker for beautiful mock data
#fake = Faker()
# Set seed for reproducible realistic names
#Faker.seed(42)


class Candidate(TypedDict):
    id: str
    name: str
    party: str
    avatar: str
    votes: int
    bio: str
    agenda: str


class AppState(rx.State):

    items: list = []
    new_item: str = ""

    def load_items(self):
        self.items = [str(item["name"]) for item in collection.find()]

    def set_new_item(self, value: str):
        self.new_item = value

    def add_item(self):
        if self.new_item:
            collection.insert_one({"name": self.new_item})
            self.new_item = ""
            self.load_items()

    # Navigation and UI controls
    current_view: str = "voting"  # "voting" or "results"
    sidebar_open: bool = True

    # Security validation state
    voter_token_input: str = ""
    is_token_valid: bool = False
    show_security_modal: bool = False
    selected_candidate_id: str = ""

    # Voting-specific states
    candidates: list[Candidate] = [
        {
            "id": "1",
            "name": "Dr. Clara Sterling",
            "party": "Future Forward Party",
            "avatar": "https://api.dicebear.com/9.x/notionists/svg?seed=Clara",
            "votes": 1420,
            "bio": "Environmental scientist & tech ethicist with 15 years in sustainable policy.",
            "agenda": "Transition to 100% clean grid, expand municipal digital infrastructure, and fund tech education.",
        },
        {
            "id": "2",
            "name": "Marcus Vance",
            "party": "Civic Alliance",
            "avatar": "https://api.dicebear.com/9.x/notionists/svg?seed=Marcus",
            "votes": 1180,
            "bio": "Former city controller and community organizer with background in economics.",
            "agenda": "Streamline small business licensing, modernize public transit pathways, and balanced budgets.",
        },
        {
            "id": "3",
            "name": "Aria Montgomery",
            "party": "Digital Democracy Coalition",
            "avatar": "https://api.dicebear.com/9.x/notionists/svg?seed=Aria",
            "votes": 950,
            "bio": "Tech founder focused on secure voting architectures & citizen participation platforms.",
            "agenda": "Implement liquid voting options, open-source city administration dashboards, and community-led budgets.",
        },
        {
            "id": "4",
            "name": "Jonathan Vance",
            "party": "Traditional Liberty",
            "avatar": "https://api.dicebear.com/9.x/notionists/svg?seed=Jonathan",
            "votes": 810,
            "bio": "Local business owner with passion for regional heritage and historic conservation.",
            "agenda": "Tax incentives for local historic businesses, streamlined municipal services, and green-space security.",
        },
    ]

    # Track voter status
    user_voted: bool = False
    voted_candidate_id: str = ""

    @rx.var
    def total_votes(self) -> int:
        return sum(c["votes"] for c in self.candidates)

    @rx.var
    def leading_candidate(self) -> str:
        if not self.candidates:
            return "None"
        # Find candidate with highest votes
        best = self.candidates[0]
        for c in self.candidates:
            if c["votes"] > best["votes"]:
                best = c
        return f"{best['name']} ({best['party']})"

    @rx.event
    def select_view(self, view_name: str):
        self.current_view = view_name

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def set_token_input(self, val: str):
        self.voter_token_input = val
        # Token must be exactly 8 digits or letters as simulated keycard validation
        if len(val) >= 6:
            self.is_token_valid = True
        else:
            self.is_token_valid = False

    @rx.event
    def open_vote_dialog(self, candidate_id: str):
        if self.user_voted:
            yield rx.toast(
                "You have already voted in this session! Multiple voting is prohibited.",
                duration=4000,
                close_button=True,
            )
            return
        self.selected_candidate_id = candidate_id
        self.voter_token_input = ""
        self.is_token_valid = False
        self.show_security_modal = True

    @rx.event
    def close_vote_dialog(self):
        self.show_security_modal = False
        self.selected_candidate_id = ""

    @rx.event
    def submit_secure_vote(self):
        if not self.is_token_valid:
            yield rx.toast(
                "Invalid Security Token! Must be at least 6 characters.",
                duration=4000,
                close_button=True,
            )
            return

        candidate_id = self.selected_candidate_id
        updated_candidates = []
        candidate_name = ""
        for c in self.candidates:
            if c["id"] == candidate_id:
                c["votes"] += 1
                candidate_name = c["name"]
            updated_candidates.append(c)

        self.candidates = updated_candidates
        self.user_voted = True
        self.voted_candidate_id = candidate_id
        self.show_security_modal = False

        yield rx.toast(
            f"Successfully Verified & Cast vote for {candidate_name}!",
            duration=5000,
            close_button=True,
        )
        self.current_view = "results"

