-- name: get-total-posts-today$
select count(*) qty_posts from post 
where datetime_creation >= curdate() 
and user_id = :user_id

-- name: get-total-posts$
select count(*) as qty_posts
from (  /*Direct Posts*/
        select * from post p where user_id  = :user_id
        union 
        /*Reposts*/
        select r.* from post p 
        left join post r on r.repost_from_id = p.id 
        where p.user_id  = :user_id
        union 
        /*Quotes*/
        select q.* from post p 
        left join post q on q.quote_from_id = p.id 
        where p.user_id  = :user_id
) user_posts

-- name: get-homepage
select user_id, post, quote_from_id, quote_from, repost_from_id, repost_from, datetime_creation
from (
	/*posts*/
	select user_id, text as post, null quote_from_id, null as quote_from, null as repost_from_id, null as repost_from, datetime_creation from post 
	where repost_from_id is null and quote_from_id is null
	/*repost*/
	union
	select r.user_id, r.text as post, null quote_from_id, null as quote_from, r.repost_from_id, p.text as repost_from, r.datetime_creation
	from post r
	inner join post p on r.repost_from_id = p.id
	/*quote*/
	union
	select q.user_id, q.text as post, q.quote_from_id, p.text as quote_from, null as repost_from_id, null as repost_from, q.datetime_creation
	from post q
	inner join post p on q.quote_from_id = p.id
) homepage
where user_id = :user_id or :user_id is null
order by datetime_creation desc

-- name: add-article-to-favorites!
INSERT INTO favorites (user_id, article_id)
VALUES ((SELECT id FROM users WHERE username = :username),
        (SELECT id FROM articles WHERE slug = :slug))
ON CONFLICT DO NOTHING;

-- name: remove-article-from-favorites!
DELETE
FROM favorites
WHERE user_id = (SELECT id FROM users WHERE username = :username)
  AND article_id = (SELECT id FROM articles WHERE slug = :slug);

-- name: is-article-in-favorites^
SELECT CASE WHEN count(user_id) > 0 THEN TRUE ELSE FALSE END AS favorited
FROM favorites
WHERE user_id = (SELECT id FROM users WHERE username = :username)
  AND article_id = (SELECT id FROM articles WHERE slug = :slug);

-- name: get-tags-for-article-by-slug
SELECT t.tag
FROM tags t
         INNER JOIN articles_to_tags att ON
        t.tag = att.tag
        AND
        att.article_id = (SELECT id FROM articles WHERE slug = :slug);

-- name: get-article-by-slug^
SELECT id,
       slug,
       title,
       description,
       body,
       created_at,
       updated_at,
       (SELECT username FROM users WHERE id = author_id) AS author_username
FROM articles
WHERE slug = :slug
LIMIT 1;

-- name: create-new-article<!
WITH author_subquery AS (
    SELECT id, username
    FROM users
    WHERE username = :author_username
)
INSERT
INTO articles (slug, title, description, body, author_id)
VALUES (:slug, :title, :description, :body, (SELECT id FROM author_subquery))
RETURNING
    id,
    slug,
    title,
    description,
    body,
        (SELECT username FROM author_subquery) as author_username,
    created_at,
    updated_at;

-- name: add-tags-to-article*!
INSERT INTO articles_to_tags (article_id, tag)
VALUES ((SELECT id FROM articles WHERE slug = :slug),
        (SELECT tag FROM tags WHERE tag = :tag))
ON CONFLICT DO NOTHING;

-- name: update-article<!
UPDATE articles
SET slug        = :new_slug,
    title       = :new_title,
    body        = :new_body,
    description = :new_description
WHERE slug = :slug
  AND author_id = (SELECT id FROM users WHERE username = :author_username)
RETURNING updated_at;

-- name: delete-article!
DELETE
FROM articles
WHERE slug = :slug
  AND author_id = (SELECT id FROM users WHERE username = :author_username);

-- name: get-articles-for-feed
SELECT a.id,
       a.slug,
       a.title,
       a.description,
       a.body,
       a.created_at,
       a.updated_at,
       (
           SELECT username
           FROM users
           WHERE id = a.author_id
       ) AS author_username
FROM articles a
         INNER JOIN followers_to_followings f ON
        f.following_id = a.author_id AND
        f.follower_id = (SELECT id FROM users WHERE username = :follower_username)
ORDER BY a.created_at
LIMIT :limit
OFFSET
:offset;
