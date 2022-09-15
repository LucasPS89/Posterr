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