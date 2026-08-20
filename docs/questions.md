1. What is the median time it takes for a first review comment by a human, on a PR opened by a human, per repo, in the past 90 days?
    id, number, created_at, draft, second fetch for formal reviews (/pulls/{number}/reviews)

2. What PR labels (bug reports, feature requests, issues, etc.) often take the longest to be merged (from creation time), in a repo, in the last 12 months?
    id, number, labels, created_at, merged_at, closed_at

3. What is the median size of a PR in terms of how many lines of code are in them, based on changed lines, per repo?
    id, number, (still missing additions, deletions, changed_files)

4. [How concentrated is the work?] What percentage of all merges in the repo-month came from the top 3 users that have the most merges?
    id, number, user (and user.type buried inside to filter bots)

5. For each repo-month, what is the median time-to-first-review, and how does it compare to the same repo three months prior — expressed as a percent change?
    id, number, created_at, second fetch for formal reviews (/pulls/{number}/reviews)

6. What is the median time it takes for a bug/issue-LABELLED PR to be merged, per repo, for PRs opened in the last 12 months?
    id, number, created_at, merged_at, closed_at, state

7. What is the median time it takes for a bug/issue-LABELLED PR to be closed unmerged, per repo, for PRs opened in the last 12 months?
    id, number, created_at, merged_at, closed_at, state


dict_keys(['url', 'id', 'node_id', 'html_url', 'diff_url', 'patch_url', 'issue_url', 'number', 'state', 'locked', 'title', 'user', 'body', 'created_at', 'updated_at', 'closed_at', 'merged_at', 'merge_commit_sha', 'assignees', 'requested_reviewers', 'requested_teams', 'labels', 'milestone', 'draft', 'commits_url', 'review_comments_url', 'review_comment_url', 'comments_url', 'statuses_url', 'head', 'base', '_links', 'author_association', 'auto_merge', 'assignee', 'active_lock_reason'])