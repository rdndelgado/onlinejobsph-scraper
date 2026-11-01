from bs4 import BeautifulSoup


def parse_job(html, url):
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.find("h1", class_="job__title")
    description_tag = soup.find("p", id="job-description")

    job_id = ""
    if title_tag and title_tag.get("data-jobid"):
        job_id = title_tag["data-jobid"]
    elif description_tag and description_tag.get("data-jobid"):
        job_id = description_tag["data-jobid"]

    field_map = {}
    for dd in soup.find_all("dd"):
        label_tag = dd.find("h3")
        value_tag = dd.find("p")
        if label_tag and value_tag:
            field_map[label_tag.get_text(strip=True).upper()] = value_tag.get_text(strip=True)

    skills = [a.get_text(strip=True) for a in soup.find_all("a", class_="card-worker-topskill")]

    return {
        "job_id": job_id,
        "url": url,
        "title": title_tag.get_text(strip=True) if title_tag else "",
        "description": description_tag.get_text(separator="\n", strip=True) if description_tag else "",
        "rate": field_map.get("WAGE / SALARY", ""),
        "job_type": field_map.get("TYPE OF WORK", ""),
        "date_updated": field_map.get("DATE UPDATED", ""),
        "skills": skills,
        "employer_name": "",  # not shown pre-login
    }
