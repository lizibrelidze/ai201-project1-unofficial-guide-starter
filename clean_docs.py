"""
Clean raw source documents: strip nav, footers, boilerplate.
Outputs cleaned .txt files to documents/
"""
import re
import os

SRC = "/Users/lizibrelidze/Library/Mobile Documents/com~apple~TextEdit/Documents"
DST = "/Users/lizibrelidze/ai201-project1-unofficial-guide-starter/documents"

os.makedirs(DST, exist_ok=True)

# ── helpers ─────────────────────────────────────────────────────────────────

def collapse_blank(text, max_blank=2):
    """Collapse runs of blank lines to at most max_blank."""
    lines = text.split("\n")
    out, blank = [], 0
    for ln in lines:
        if ln.strip() == "":
            blank += 1
            if blank <= max_blank:
                out.append("")
        else:
            blank = 0
            out.append(ln)
    return "\n".join(out).strip()

# ── GreekRank cleaner ────────────────────────────────────────────────────────

# Lines/blocks that are purely boilerplate on every GreekRank page
GR_STRIP_EXACT = {
    "Greekrank Logo", "Search for a University/School", "LoginRegister",
    "Universities", "Fraternities", "Sororities", "Rankings", "Request",
    "Contact Us", "Overview", "Discussion", "News", "School",
    "Greek Rank", "Information", "Ratings",
    "Filter By:", "Sort By:", "None", "Newest First", "Oldest First",
    "Rating (High to Low)", "Rating (Low to High)",
    "Respond", "Report",
    "↓ Posts Continued Below ↓",
    "YOU MAY ALSO LIKE", "NEW ON GREEKRANK", "POPULAR ON GREEKRANK",
    "Follow GreekRank Facebook     Follow GreekRank Twitter    ",
    "Site Links", "Contact", "Advertise", "Resources", "About Us",
    "Terms of Use", "Privacy Policy", "Legal", "© 2025 - Greekrank",
    "Rate this Sorority", "  Rate this Sorority",
    "NEW!  Be notified when someone leaves a new rating! Alert Me",
    "Associates with:",
    "Reputation:", "Friendliness:", "Popularity:", "Classiness:",
    "Involvement:", "Social Life:", "Sisterhood:",
    "Reputation:  Smart", "Reputation:  Looks", "Reputation:  Social",
    "Reputation:  Wealthy", "Reputation:  Athletic",
    "Friendliness:  ", "Popularity:  ", "Classiness:  ",
    "Involvement:  ", "Social Life:  ", "Sisterhood:  ",
    " ", "\xa0",
    "Request", "Didn't find your school?",
    "Request for your school to be featured on GreekRank.",
    # sorority/org name headers (vary per file, handled via startswith too)
    "Alpha sigma Alpha", "Alpha Sigma Alpha", "Delta Zeta",
    "Delta Phi Epsilon", "Phi Sigma Sigma",
    "Delta Sigma Pi Fraternity", "Sigma Alpha Mu Fraternity",
    "Lambda Chi Alpha Fraternity", "Phi Kappa Psi Fraternity",
    "Phi Sigma Kappa Fraternity", "Pi Kappa Alpha Fraternity",
    "Tau Kappa Epsilon Fraternity", "Theta Chi Fraternity",
    "Kappa Alpha Order Fraternity",
}

GR_STRIP_STARTSWITH = (
    "Home    Universities",
    "Alpha Sigma Alpha - ΑΣΑ Sorority Ratings",
    "Delta Zeta - ΔΖ Sorority Ratings",
    "Delta Phi Epsilon - ΔΦΕ Sorority Ratings",
    "Phi Sigma Sigma - ΦΣΣ Sorority Ratings",
    "Total Ratings:", "Ratings\n", "Information\n",
    "Sorority Name:", "School: Drexel",
    "Associates with:\n- Fraternities:", "Associates with:\n- Sororities:",
    "- Fraternities:", "- Sororities:",
    "Page ", "FIRST  <", "1  2  3", "YOU MAY ALSO", "NEW ON GREEK",
    "POPULAR ON",
    "No Responses", "Respond  ", "Vote review",
    "Follow GreekRank",
    "© 2025",
    "NEW! ", # image alt-text lines
)

GR_STRIP_REGEX = [
    re.compile(r'^\d+Vote review (up|down)$'),
    re.compile(r'^Respond\s+(No Responses|\d+ Response)'),
    re.compile(r'^\d+ Response'),
    re.compile(r'^FIRST\s*<\s*PREV'),
    re.compile(r'^\d\s+\d\s+\d'),          # pagination like "1  2  3"
    re.compile(r'^Page \d+ of \d+'),
    re.compile(r'^\d+Vote'),
    re.compile(r'^Associates with:$'),
    re.compile(r'^(Alpha|Delta|Lambda|Pi|Sigma|Phi|Theta|Tau|Kappa)\s+\S+.*(Fraternity|Sorority)$'),
    # Stats lines like "Reputation:Smart Friendliness:79.2% ..."
    re.compile(r'^Reputation:\w+\s+Friendliness:'),
    # "161 Ratings" type summary lines
    re.compile(r'^\d+ Ratings?$'),
]


def clean_greekrank(raw_text, sorority_name):
    """Keep only review entries: rating, tier, reviewer, date, review body."""
    lines = raw_text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i].strip()
        # Skip blank / pure whitespace
        if not ln:
            out.append("")
            i += 1
            continue
        # Skip exact matches
        if ln in GR_STRIP_EXACT:
            i += 1
            continue
        # Skip starts-with patterns
        skip = False
        for pat in GR_STRIP_STARTSWITH:
            if ln.startswith(pat):
                skip = True
                break
        if skip:
            i += 1
            continue
        # Skip regex patterns
        for rx in GR_STRIP_REGEX:
            if rx.match(ln):
                skip = True
                break
        if skip:
            i += 1
            continue
        # Skip GreekRank article thumbnail alt-text lines (image caption + article title)
        if re.search(
            r'(Students walking|College students|sorority row|fraternity house'
            r'|Greek chapter house|chapter house on a college'
            r'|exterior view of a sorority|sorority house at \w+ University'
            r'|representing the departure|Stanford\'s Sorority|Sorority Exodus'
            r'|Students participating in Greek Week'
            r'|Fraternity brothers gathered'
            r'|Greek Week Still Hits|Hits Different at Small'
            r'|living with \d+ guys|survival course'
            r'|chapter house vs|off-campus.*honest breakdown'
            r'|dirty rush is real)',
            ln, re.I
        ):
            i += 1
            continue
        # Skip lines that are just image captions / NEW! article links
        if " NEW! " in ln and ("Stanford" in ln or "Hazing" in ln or "Greek" in ln
                                or "Sorority" in ln or "Fraternity" in ln):
            i += 1
            continue
        # Keep the line
        out.append(lines[i])
        i += 1

    # Prepend context header
    header = f"Source: GreekRank reviews for {sorority_name} at Drexel University\n"
    return header + collapse_blank("\n".join(out))


# ── Reddit cleaner ───────────────────────────────────────────────────────────

REDDIT_STRIP_EXACT = {
    "Skip to main content", "Skip to Navigation", "Skip to Right Sidebar",
    "Back", "Sort by:", "Best", "Search Comments", "Expand comment search",
    "Comments Section", "Join the conversation", "Upvote", "Downvote",
    "Reply", "Award", "Share", "Go to comments", "Advertise on Reddit",
    "Open chat", "Create", "Create post", "Open inbox", "Expand user menu",
    "Collapse Navigation", "Community Info Section", "User flair",
    "r/Drexel Rules", "Discord", "Drexel Links", "Moderators", "Message Mods",
    "View all moderators", "Reddit Rules", "Privacy Policy", "User Agreement",
    "Your Privacy Choices", "Accessibility",
    "No harassment, discrimination or abuse of any kind",
    "No spam", "No advertising", "No NSFW content",
    "No sharing of illegal content", "No sharing of private information",
    "No trolling or heavy politics",
    "Please keep in mind of Academic Dishonesty",
    "Website", "Facebook", "Twitter", "Instagram",
    "Term Master Schedule (TMS)", "Academic Calendar", "Campus Map",
    "Elective Dashboard",
    "Show more", "Created Jan 25, 2008", "Public",
    "Joined", "Drexel University",
    "Drexel University, home of the Drexel Dragons! A community to discuss academics, career, and campus life located at the Avenue of Technology.",
}

REDDIT_STRIP_STARTSWITH = (
    "r/Drexel", "Reddit, Inc. ©", "u/", "Go to Drexel",
    "•", "10K", "178",
)


def clean_reddit(raw_text):
    lines = raw_text.split("\n")
    out = []
    for ln in lines:
        s = ln.strip()
        if not s:
            out.append("")
            continue
        if s in REDDIT_STRIP_EXACT:
            continue
        skip = any(s.startswith(p) for p in REDDIT_STRIP_STARTSWITH)
        if skip:
            continue
        # Skip pure numbers (vote counts, member counts)
        if re.match(r'^\d+$', s):
            continue
        # Skip relative time stamps like "3y ago", "4y ago", "1y ago"
        if re.match(r'^\d+[ydmh] ago$', s):
            continue
        out.append(ln)
    return "Source: Reddit r/Drexel discussions about sororities\n" + collapse_blank("\n".join(out))


# ── Recruitment page cleaner ─────────────────────────────────────────────────

def clean_recruitment(raw_text):
    """Keep registration info and recruitment schedule."""
    lines = raw_text.split("\n")
    out = []
    strip_exact = {
        "Get Started", "Request a Demo", "Sign Up", "Login", "Logout",
        "Explore", "Home", "Support", "Help & Support", "Company", "About",
        "PhiredUp logo", "CampusDirector logo", "© PhiredUp 2026",
        "CampusDirector logo",
        "If you have already signed up, click here to login to your account.",
        "Next tell us a little about yourself:",
        "Select what best describes you", "I'm a...",
        "Choose from the dropdown list what best describes you.",
        "Need help? Click here to contact support.",
        "Log In",
    }
    for ln in lines:
        s = ln.strip()
        if not s or s in strip_exact:
            continue
        out.append(ln)
    return "Source: Drexel Panhellenic recruitment registration page (Fall 2026)\n" + collapse_blank("\n".join(out))


# ── National org website cleaner ─────────────────────────────────────────────

def clean_national_org(raw_text, org_name):
    """Strip all nav/footer boilerplate from national org websites.
    Keep: About/mission text and Drexel chapter DragonLink description.
    """
    lines = raw_text.split("\n")
    nav_keywords = {
        "SHOP", "MYDPHIE", "EVENTS", "KNOWLEDGE CENTER", "POLICIES",
        "ALUMNAE DUES", "DONATE", "logo", "Who We Are", "Why DPhiE",
        "Get Involved", "Stay Connected", "Give Back", "Chapter Locator",
        "Programming", "Latest News", "Donate Now",
        "Social Justice Series", "International Leadership Forum",
        "Dimes for DPhiE", "Contact Info", "Stay in Touch",
        "Click here to update your contact information.",
        "Delta Phi Epsilon Educational Foundation",
        "© Delta Phi Epsilon International Sorority.",
        "215.732.5901", "215.732.5906", "info@dphie.org",
        "251 S. Camac Street", "Philadelphia, PA 19107",
        "Alumnae Dues", "Find a Chapter", "Give", "Library", "Member Login",
        "en", "Arabic", "Chinese (Simplified)", "Dutch", "English", "French",
        "German", "Italian", "Portuguese", "Russian", "Spanish",
        "Delta Gamma Logo", "About Us", "Who We Are", "Our History",
        "Notable Delta Gammas", "Our Leadership", "Our Philanthropy",
        "Belonging", "Collegians", "Collegiate Experience", "Chapter Housing",
        "Parents & Families", "Personal and Professional Growth Opportunities",
        "Alumnae", "Alumnae Experience", "Alumna Initiate Program",
        "Find an Alumnae Group", "Pay Your Dues", "Recent Graduates",
        "Volunteer", "miniMBA", "Recommend a Potential New Member",
        "Collegiate Development Consultants", "Foundation", "About the Foundation",
        "Donor Recognition", "Impact", "Individual Member Support",
        "Training and Programming", "Service for Sight", "Lectureships",
        "Ways to Give", "News + Events", "Events", "News", "ANCHORA",
        "Join Our Sisterhood", "Follow the Fraternity",
        "End of post.", "Powered by Curator.io",
        "3250 Riverside Drive", "Columbus, OH 43221", "614-481-8169",
        "Fraternity", "Contact Us", "Anchorbase", "The Pursuit",
        "Chapter Locator", "Shop Hannah's Closet", "Greek Licensing",
        "Campus Partners", "Careers", "The Do", "Good Sisterhood.",
        "© 2026. All Rights Reserved.",
        "MEMBER LOG IN", "SUBMIT A CONCERN", "DONATE NOW",
        "ABOUT US", "PROGRAMS", "PARTNERS", "HOUSING", "FOUNDATION",
        "NEWS", "CONTACT US", "WE ARE PHI SIGMA SIGMA",
        "FRIENDSHIP, FAITH, LOVE, SINCERITY, INTEGRITY & STRENGTH",
        "FIND A", "CHAPTER", "ENGAGE OR VOLUNTEER",
        "INTERNATIONAL HEADQUARTERS", "(410) 799-1224",
        "Phi Sigma Sigma, Inc.", "1213 Liberty Rd, Suite J #335",
        "Eldersburg, MD 21784", "Emergency Line: (410) 530-1913",
        "PhiSigHQ@phisigmasigma.org", "UPDATE CONTACT INFO", "FOLLOW US",
        "White Instagram Icon", "White Facebook Icon",
        "© 2025 by Phi Sigma Sigma, Inc.",
        "Skip to Main Content", "600_PSS CENTER (4).png",
        "Open Main Navigation",
        "1900", "1910", "1920", "1930", "1940", "1950",
        "1960", "1970", "1980", "1990", "2000", "2010", "2020",
        "Read more", "link arrow",
        "Footer Logo", "Update Your Information",
        "9002 Vincennes Circle, Indianapolis, IN 46268-3018",
        "PH: (317) 871-2920", "FAX: (317) 871-2924",
        "MyAΣA Log In", "Officer Portal", "Contact Us", "Join",
        "Chapter Locator", "Collegiate Experience", "Chapter Commitments",
        "Member Portals and Support", "Membership Education",
        "New Member Referral", "Terminology", "Alumnae Experience",
        "Update Your Information Form", "Alumnae Dues", "Alumnae Initiation",
        "Be Involved", "Legacies", "About", "Timeline", "Service & Giving",
        "National Headquarters", "Alpha Sigma Alpha Foundation",
        "Foundation About", "Foundation Scholarships & Grants",
        "Foundation Give Back", "Foundation Volunteering", "Foundation Donate",
        "Events & Programming", "Alpha Sigma Alpha News & Media",
        "Alpha Connect Sisterhood Series Podcast", "Alpha Sigma Alpha Brand",
        "Shop", "© Alpha Sigma Alpha", "Brand Guidelines",
        "Privacy Policy and Terms of Service",
        # DZ boilerplate
        "We value your privacy",
        "We use cookies to enhance your browsing experience, serve personalized ads or content, and analyze our traffic. By clicking \"Accept All\", you consent to our use of cookies.",
        "Customize", "Reject All", "Accept All",
        "Skip to content", "SearchSearch", "Search", "Close",
        "Member Experience", "News & Events", "Service & Philanthropy",
        "Read More", "Read", "Learn", "Join", "Connect", "Reconnect",
        "Delta Zeta Women's Membership Organization | Delta Zeta Sorority",
        "Delta Zeta National Headquarters",
        "202 East Church Street", "Oxford, OH 45056",
        "(513) 523-7597", "Contact Us", "© 2026 Delta Zeta. All Rights Reserved.",
        "Brand guidelines", "Approved Vendors", "Terms of Use   |   Privacy Policy",
        " Site by Clockwork",
        # DragonLink boilerplate
        "Constitution/Bylaws", "Documents", "Public Events",
        "There are currently no upcoming events. View past events.",
        "Gallery Image", "LOADING",
    }

    out = []
    for ln in lines:
        s = ln.strip()
        if not s or s in nav_keywords:
            continue
        # Skip lines that are just phone/address numbers or navigation
        if re.match(r'^\d{3}[-.\s]\d{3}[-.\s]\d{4}$', s):
            continue
        # Skip year-only lines from ASA history timeline
        if re.match(r'^\d{4}$', s):
            continue
        # Skip "Drexel WebsiteL DragonLink" type lines
        if "DragonLink" in s and len(s) < 30:
            continue
        if s in ("Drexel website:", "Drexel WebsiteL DragonLink"):
            continue
        out.append(ln)

    return f"Source: {org_name} official information (national website + Drexel chapter DragonLink)\n" + collapse_blank("\n".join(out))


# ── PHC cleaner ──────────────────────────────────────────────────────────────

def clean_phc(raw_text):
    lines = raw_text.split("\n")
    out = []
    for ln in lines:
        s = ln.strip()
        if not s:
            out.append("")
            continue
        if s in ("SHARE", "ecognized PHC Sororities", "Recognized PHC Sororities"):
            continue
        out.append(ln)
    # Deduplicate (the file has the block twice)
    content = collapse_blank("\n".join(out))
    # Simple dedup: keep first occurrence of each non-blank line
    seen, deduped = set(), []
    for ln in content.split("\n"):
        key = ln.strip()
        if key and key in seen:
            continue
        seen.add(key)
        deduped.append(ln)
    return "Source: Drexel Panhellenic Council - recognized PHC sororities list\n" + collapse_blank("\n".join(deduped))


# ── College Confidential cleaner ─────────────────────────────────────────────

def clean_college_confidential(raw_text):
    """Keep post text; strip nav, sidebar, suggested-threads table, footer."""
    CC_STRIP = {
        "Skip to where you left off (last reply, post 3)", "Skip to top",
        "Skip to main content", "Community", "All Forums",
        "Applying to College", "College Search & Selection",
        "Chance Me / Match Me", "Paying for College", "Parents Forum",
        "CC Official Store", "Events", "College", "College Directory A-Z",
        "Colleges (20-59% Acceptance)", "Colleges (60-100% Acceptance)",
        "Top Pre-Med Colleges (>20% Acceptance)",
        "Top Law Colleges (>20% Acceptance)", "Resources", "Article Library",
        "FREE Essay Review", "2025–2026 Decisions Calendar", "Campus Tours",
        "Paying for College Guide", "Scholarship Search", "Sign Up", "Log In",
        "Reply", "Suggested Threads",
        "Topic list, column headers with buttons are sortable.", "Thread",
        "Replies", "Views", "Activity",
        "About Us", "Forum Rules", "Partner With Us", "Privacy Policy",
        "Press Inquiries", "Terms of Service",
        "Do Not Share My Personal Information", "COMMUNITY",
        "COLLEGES", "RESOURCES", "SCHOLARSHIP SEARCH", "CONNECT WITH US",
        "© 2026 College Confidential, LLC. All Rights Reserved.",
        "Cookie Settings", "Colleges & Universities",
        "Want to read more? Browse other topics in",
        "or view latest topics.",
        "10 years later", "Closed on Apr 17, 2021",
        "The 2027 AMCAS application is now open for applicants entering "
        "medical school in fall 2027! Find answers to your questions, connect "
        "with other applicants, and seek guidance from our experts in the "
        "Pre-Med & Medical School forums.",
        "views",
    }
    lines = raw_text.split("\n")
    out = []
    for ln in lines:
        s = ln.strip()
        if not s or s in CC_STRIP:
            continue
        if s.startswith("•"):
            continue
        if re.match(r'^\d+[km]?$', s, re.I):
            continue
        if re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{2,4}$', s):
            continue
        if re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}$', s):
            continue
        if re.match(r'^\d+[dywmh]$', s):
            continue
        out.append(ln)
    cleaned = "\n".join(out)
    cleaned = re.sub(r'<[^>]+>', '', cleaned)  # strip HTML tags
    return "Source: College Confidential forum - Drexel sorority discussion\n" + collapse_blank(cleaned)


# ── file map ─────────────────────────────────────────────────────────────────

FILES = {
    "Apha Sigma Alpha Greek Rank.txt": (
        "greekrank",
        "Alpha Sigma Alpha",
        "asa_greekrank.txt",
    ),
    "Greek Rank delta phi.txt": (
        "greekrank",
        "Delta Phi Epsilon",
        "dphie_greekrank.txt",
    ),
    "Delta Zeta Greek Rank.txt": (
        "greekrank",
        "Delta Zeta",
        "dz_greekrank.txt",
    ),
    "Phi Sigma Sigma Greek Rank.txt": (
        "greekrank",
        "Phi Sigma Sigma",
        "phisig_greekrank.txt",
    ),
    "Reddit post about sororities.txt": (
        "reddit",
        None,
        "reddit_sororities.txt",
    ),
    "Recrutment drexel 2026-2027.txt": (
        "recruitment",
        None,
        "recruitment_2026.txt",
    ),
    "DrexelPHC.txt": (
        "phc",
        None,
        "drexel_phc.txt",
    ),
    # National org + DragonLink pages — keep Drexel chapter description only
    "Delta Phie Drexel.txt": (
        "national",
        "Delta Phi Epsilon at Drexel University",
        "dphie_about.txt",
    ),
    "Delta Zeta Drexel.txt": (
        "national",
        "Delta Zeta at Drexel University",
        "dz_about.txt",
    ),
    "Deltagamma Drexel.txt": (
        "national",
        "Delta Gamma at Drexel University",
        "dg_about.txt",
    ),
    "Drexel ASA.txt": (
        "national",
        "Alpha Sigma Alpha at Drexel University",
        "asa_about.txt",
    ),
    "Phi Sigma Sigma Drexek.txt": (
        "national",
        "Phi Sigma Sigma at Drexel University",
        "phisig_about.txt",
    ),
    "Make Confidence.txt": (
        "cc_forum",
        None,
        "cc_drexel_sorority.txt",
    ),
}

for src_name, (kind, label, dst_name) in FILES.items():
    src_path = os.path.join(SRC, src_name)
    dst_path = os.path.join(DST, dst_name)
    with open(src_path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    if kind == "greekrank":
        cleaned = clean_greekrank(raw, label)
    elif kind == "reddit":
        cleaned = clean_reddit(raw)
    elif kind == "recruitment":
        cleaned = clean_recruitment(raw)
    elif kind == "phc":
        cleaned = clean_phc(raw)
    elif kind == "cc_forum":
        cleaned = clean_college_confidential(raw)
    else:  # national
        cleaned = clean_national_org(raw, label)

    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    wc = len(cleaned.split())
    print(f"  {dst_name}: {wc} words")

print("\nDone. Printing first 60 lines of asa_greekrank.txt to verify:\n")
with open(os.path.join(DST, "asa_greekrank.txt")) as f:
    for i, line in enumerate(f):
        if i >= 60:
            break
        print(line, end="")
