import os
import random
import string
import pandas as pd
import numpy as np

# Sample realistic vocabularies for dummy data creation
FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Carol", "Kevin", "Amanda", "Brian", "Dorothy", "George", "Melissa",
    "Timothy", "Deborah", "Ronald", "Stephanie", "Edward", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy", "Jacob",
    "Priya", "Rahul", "Aarav", "Ananya", "Vikram", "Neha", "Arjun", "Kavya", "Carlos",
    "Sofia", "Mateo", "Isabella", "Alejandro", "Camila", "Wei", "Ying", "Ming", "Jing"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Patel", "Sharma", "Kumar", "Singh", "Gupta", "Chen", "Wang", "Zhang", "Liu"
]

CITIES_STATES_ZIPS = [
    ("New York", "NY", "10001"), ("Los Angeles", "CA", "90001"), ("Chicago", "IL", "60601"),
    ("Houston", "TX", "77001"), ("Phoenix", "AZ", "85001"), ("Philadelphia", "PA", "19101"),
    ("San Antonio", "TX", "78201"), ("San Diego", "CA", "92101"), ("Dallas", "TX", "75201"),
    ("San Jose", "CA", "95101"), ("Austin", "TX", "78701"), ("Jacksonville", "FL", "32201"),
    ("Fort Worth", "TX", "76101"), ("Columbus", "OH", "43201"), ("Charlotte", "NC", "28201"),
    ("San Francisco", "CA", "94101"), ("Indianapolis", "IN", "46201"), ("Seattle", "WA", "98101"),
    ("Denver", "CO", "80201"), ("Washington", "DC", "20001"), ("Boston", "MA", "02101"),
    ("El Paso", "TX", "79901"), ("Nashville", "TN", "37201"), ("Detroit", "MI", "48201"),
    ("Oklahoma City", "OK", "73101"), ("Portland", "OR", "97201"), ("Las Vegas", "NV", "89101")
]


def _introduce_typo(text: str) -> str:
    """Randomly delete, substitute, transpose, or insert a character in text."""
    if not text or len(text) <= 1:
        return text

    op = random.choice(["substitute", "delete", "transpose", "insert"])
    pos = random.randint(0, len(text) - 1)

    if op == "substitute":
        rand_char = random.choice(string.ascii_lowercase)
        return text[:pos] + rand_char + text[pos + 1:]
    elif op == "delete":
        return text[:pos] + text[pos + 1:]
    elif op == "transpose" and pos < len(text) - 1:
        return text[:pos] + text[pos + 1] + text[pos] + text[pos + 2:]
    elif op == "insert":
        rand_char = random.choice(string.ascii_lowercase)
        return text[:pos] + rand_char + text[pos:]
    return text


def _corrupt_date(dob_str: str) -> str:
    """Randomly modify year, month, or day in YYYY-MM-DD string."""
    try:
        parts = dob_str.split("-")
        if len(parts) != 3:
            return dob_str
        y, m, d = parts
        choice = random.choice(["swap_md", "alter_year", "alter_day"])
        if choice == "swap_md" and int(d) <= 12 and int(m) <= 12:
            return f"{y}-{d.zfill(2)}-{m.zfill(2)}"
        elif choice == "alter_year":
            new_y = str(int(y) + random.choice([-1, 1, 10, -10]))
            return f"{new_y}-{m}-{d}"
        else:
            new_d = str(max(1, min(28, int(d) + random.choice([-1, 1]))))
            return f"{y}-{m}-{new_d.zfill(2)}"
    except Exception:
        return dob_str


def generate_dummy_datasets(
    output_dir: str = ".",
    n_a: int = 500,
    n_b: int = 400,
    match_ratio: float = 0.7,
    noise_level: float = 0.35,
    seed: int = 42
):
    """
    Generates synthetic datasets for record linkage benchmarking.
    
    Args:
        output_dir: Directory where CSV files will be saved.
        n_a: Number of records in Dataset A.
        n_b: Number of records in Dataset B.
        match_ratio: Fraction of records in B that correspond to records in A.
        noise_level: Probability of corrupting each field in matching records.
        seed: Random seed for reproducibility.
    """
    random.seed(seed)
    np.random.seed(seed)
    os.makedirs(output_dir, exist_ok=True)

    records_a = []
    for i in range(1, n_a + 1):
        rec_id = f"A{i:04d}"
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        year = random.randint(1950, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        dob = f"{year}-{month:02d}-{day:02d}"
        city, state, zip_code = random.choice(CITIES_STATES_ZIPS)
        phone = f"{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
        email = f"{fname.lower()}.{lname.lower()}{random.randint(1,99)}@example.com"
        
        records_a.append({
            "id": rec_id,
            "first_name": fname,
            "last_name": lname,
            "dob": dob,
            "zip_code": zip_code,
            "city": city,
            "state": state,
            "phone": phone,
            "email": email
        })

    df_a = pd.DataFrame(records_a)

    # Generate Dataset B and Ground Truth
    records_b = []
    ground_truth = []

    n_matches = int(n_b * match_ratio)
    matching_indices_a = random.sample(range(n_a), n_matches)

    b_counter = 1
    for idx_a in matching_indices_a:
        rec_a = records_a[idx_a]
        rec_b_id = f"B{b_counter:04d}"
        
        # Corrupt fields based on noise_level
        fname = rec_a["first_name"]
        lname = rec_a["last_name"]
        
        # Swapped first and last name occasionally
        if random.random() < 0.08:
            fname, lname = lname, fname
        
        if random.random() < noise_level:
            fname = _introduce_typo(fname)
        if random.random() < noise_level:
            lname = _introduce_typo(lname)
            
        dob = rec_a["dob"]
        if random.random() < noise_level:
            dob = _corrupt_date(dob)

        zip_code = rec_a["zip_code"]
        if random.random() < noise_level:
            # Change 1 digit in zip
            zip_list = list(zip_code)
            zip_list[random.randint(0, 4)] = str(random.randint(0, 9))
            zip_code = "".join(zip_list)

        city = rec_a["city"]
        if random.random() < noise_level * 0.5:
            city = _introduce_typo(city)

        state = rec_a["state"]

        phone = rec_a["phone"]
        if random.random() < noise_level:
            # Missing phone or typo
            if random.random() < 0.5:
                phone = ""
            else:
                phone = f"{phone[:-2]}{random.randint(10,99)}"

        email = rec_a["email"]
        if random.random() < noise_level:
            email = "" if random.random() < 0.4 else _introduce_typo(email)

        records_b.append({
            "id": rec_b_id,
            "first_name": fname,
            "last_name": lname,
            "dob": dob,
            "zip_code": zip_code,
            "city": city,
            "state": state,
            "phone": phone,
            "email": email
        })

        ground_truth.append({
            "id_a": rec_a["id"],
            "id_b": rec_b_id
        })
        b_counter += 1

    # Non-matching noise records in B
    n_non_matches = n_b - n_matches
    for _ in range(n_non_matches):
        rec_b_id = f"B{b_counter:04d}"
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        year = random.randint(1950, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        dob = f"{year}-{month:02d}-{day:02d}"
        city, state, zip_code = random.choice(CITIES_STATES_ZIPS)
        phone = f"{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
        email = f"{fname.lower()}.{lname.lower()}{random.randint(100,999)}@example.com"

        records_b.append({
            "id": rec_b_id,
            "first_name": fname,
            "last_name": lname,
            "dob": dob,
            "zip_code": zip_code,
            "city": city,
            "state": state,
            "phone": phone,
            "email": email
        })
        b_counter += 1

    # Shuffle dataset B
    random.shuffle(records_b)
    df_b = pd.DataFrame(records_b)
    df_gt = pd.DataFrame(ground_truth)

    # Save to CSV files
    path_a = os.path.join(output_dir, "dataset_a.csv")
    path_b = os.path.join(output_dir, "dataset_b.csv")
    path_gt = os.path.join(output_dir, "ground_truth.csv")

    df_a.to_csv(path_a, index=False)
    df_b.to_csv(path_b, index=False)
    df_gt.to_csv(path_gt, index=False)

    print(f"[Data Generator] Dataset A saved: {len(df_a)} records -> {path_a}")
    print(f"[Data Generator] Dataset B saved: {len(df_b)} records -> {path_b}")
    print(f"[Data Generator] Ground Truth saved: {len(df_gt)} matching pairs -> {path_gt}")

    return df_a, df_b, df_gt


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate synthetic record linkage datasets.")
    parser.add_argument("--out", type=str, default=".", help="Output directory path")
    parser.add_argument("--na", type=int, default=500, help="Number of records in Dataset A")
    parser.add_argument("--nb", type=int, default=400, help="Number of records in Dataset B")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    generate_dummy_datasets(output_dir=args.out, n_a=args.na, n_b=args.nb, seed=args.seed)
