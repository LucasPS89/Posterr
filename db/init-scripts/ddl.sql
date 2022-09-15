drop table user;
CREATE TABLE if not exists user(
    id bigint(20) NOT NULL AUTO_INCREMENT,
    username varchar(14) NOT NULL,
    date_joined DATE not null default current_date(),
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table post;
CREATE TABLE if not exists post(
    id bigint(20) NOT NULL AUTO_INCREMENT,
    repost_from_id bigint(20), 
    quote_from_id bigint(20), 
    user_id bigint(20),
    datetime_creation TIMESTAMP NOT NULL DEFAULT NOW(),
    text varchar(777),
    PRIMARY KEY (id),
    FOREIGN KEY (repost_from_id) REFERENCES post(id),
    FOREIGN KEY (quote_from_id) REFERENCES post(id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    INDEX (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;