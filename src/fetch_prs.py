import json
import logging
import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from pathlib import Path

logging.basicConfig(
    level = logging.INFO, # switch to DEBUG when needed
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# PR extraction

def fetch_prs(token, owner, repo, days_back=365):
    results = []
    page_counter = 0
    now = datetime.now(timezone.utc)
    cutoff_date = now - timedelta(days=days_back)
    headers = { 
        'Authorization': f'Bearer {token}'
    }
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls?per_page=100&state=all&sort=updated&direction=desc'
    while url:
        response = requests.get(url, headers=headers)
        logger.debug(response.url)
        if response.status_code != 200:
            logger.error('Status Code: %d', response.status_code)
            break
        page_data = response.json()
        for pr in page_data:
            recent_pr_update_time = datetime.fromisoformat(pr['updated_at'])
            if recent_pr_update_time > cutoff_date:
                results.append(pr)
            else:
                return results
        page_counter += 1
        logger.info('Fetched page %d. Total PRs at: %d. Updated at: %s', page_counter, len(results), page_data[-1]['updated_at'])
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None
    return results

# transform function for desired fields (slim_prs)

def transform_prs(raw_prs):
    slim_prs = []
    for pr in raw_prs:
        slim_pr = {
            'id' : pr['id'],
            'number' : pr['number'],
            'user_login' : pr['user']['login'],
            'user_type' : pr['user']['type'],
            'created_at' : pr['created_at'],
            'merged_at' : pr['merged_at'],
            'closed_at' : pr['closed_at'],
            'updated_at' : pr['updated_at'],
            'labels' : [label['name'] for label in pr['labels']],
            'state' : pr['state'],
            'title' : pr['title'],
            'draft' : pr['draft']
        }
        slim_prs.append(slim_pr)
    return slim_prs

def write_prs(data, repo):
    now = datetime.now(timezone.utc)
    formatted_now = now.strftime("%Y%m%dT%H%M%S")

    directory = Path('data/raw')
    directory.mkdir(parents=True, exist_ok=True)
    filename = f'{repo}_{formatted_now}.json'
    fullpath = directory/filename

    with open(fullpath, 'w') as file:
        json.dump(data, file, indent=4)

    logger.info('Wrote to file %s', fullpath)
    return fullpath


if __name__ == '__main__':
    load_dotenv()

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError('Token not found in .env. Check if the file exists and token is correct.')

    owner = 'pandas-dev'
    repo = 'pandas'
    results = fetch_prs(token, owner, repo)
    logger.info('Fetched %d PRs', len(results))

    slim_prs = transform_prs(results)
    logger.info('Transformed %d Slim PRs', len(slim_prs))
    logger.debug(slim_prs[0])

    path = write_prs(repo, slim_prs)