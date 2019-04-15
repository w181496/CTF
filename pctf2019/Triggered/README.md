# Triggered

## 題目

- 給了一個plpgsql跑的microservice
- plpgsql不是一般的SQL，是postgresql搞出的一個語言
- 找一下可以發現source code: http://triggered.pwni.ng:52856/static/schema.sql
- 我們的Request/Respons和header等的處理都會先經過plpgsql才進到資料庫

## 漏洞



- 1. `POST /login`會設一個uuid到session，並綁上參數`username`指定的user
- 2. `POST /login/password`會去從session抓uuid對應的user密碼來和我們輸入的`password`比對
- 3. 密碼比對相同後，會根據uuid去UPDATE `logged_in=TRUE`

這邊存在一個Race condition漏洞

只要在2.和3.之間去另外跑1.

就能把通過密碼驗證裡session的user改成任意user

做到任意user登入

---

詳細漏洞成因可以看這段code:

```sql
CREATE TABLE web.session (
  uid uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_uid uuid,
  logged_in boolean NOT NULL DEFAULT FALSE
);


---------- POST /login

CREATE FUNCTION web.handle_post_login() RETURNS TRIGGER AS $$
DECLARE
  form_username text;
  session_uid uuid;
  form_user_uid uuid;
  context jsonb;
BEGIN
  SELECT
    web.get_form(NEW.uid, 'username')
  INTO form_username;

  SELECT
    web.get_cookie(NEW.uid, 'session')::uuid
  INTO session_uid;

  SELECT
    uid
  FROM
    web.user
  WHERE
    username = form_username
  INTO form_user_uid;

  IF form_user_uid IS NOT NULL
  THEN
    INSERT INTO web.session (
      uid,
      user_uid,
      logged_in
    ) VALUES (
      COALESCE(session_uid, uuid_generate_v4()),
      form_user_uid,
      FALSE
    )
    ON CONFLICT (uid)
      DO UPDATE
      SET
        user_uid = form_user_uid,
        logged_in = FALSE
    RETURNING uid
    INTO session_uid;

    PERFORM web.set_cookie(NEW.uid, 'session', session_uid::text);
    PERFORM web.respond_with_redirect(NEW.uid, '/login/password');
  ELSE
    PERFORM web.respond_with_redirect(NEW.uid, '/login');
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER route_post_login
  BEFORE INSERT
  ON web.request
  FOR EACH ROW
  WHEN (NEW.path = '/login' AND NEW.method = 'POST')
  EXECUTE PROCEDURE web.handle_post_login();

  ---------- POST /login/password

CREATE FUNCTION web.handle_post_login_password() RETURNS TRIGGER AS $$
DECLARE
  form_password text;
  session_uid uuid;
  success boolean;
BEGIN
  SELECT
    web.get_cookie(NEW.uid, 'session')::uuid
  INTO session_uid;

  IF session_uid IS NULL
  THEN
    PERFORM web.respond_with_redirect(NEW.uid, '/login');
    RETURN NEW;
  END IF;

  SELECT
    web.get_form(NEW.uid, 'password')
  INTO form_password;

  IF form_password IS NULL
  THEN
    PERFORM web.respond_with_redirect(NEW.uid, '/login/password');
    RETURN NEW;
  END IF;

  SELECT EXISTS (
    SELECT
      *
    FROM
      web.user usr
        INNER JOIN web.session session
          ON usr.uid = session.user_uid
    WHERE
      session.uid = session_uid
        AND usr.password_hash = crypt(form_password, usr.password_hash)
  )
  INTO success;

  IF success
  THEN
    UPDATE web.session
    SET
      logged_in = TRUE
    WHERE
      uid = session_uid;

    PERFORM web.respond_with_redirect(NEW.uid, '/');
  ELSE
    PERFORM web.respond_with_redirect(NEW.uid, '/login/password');
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER route_post_login_password
  BEFORE INSERT
  ON web.request
  FOR EACH ROW
  WHEN (NEW.path = '/login/password' AND NEW.method = 'POST')
  EXECUTE PROCEDURE web.handle_post_login_password();

```


## FLAG

登入成admin後，搜一下就能找到flag

![](https://i.imgur.com/7U7tbUd.png)

`PCTF{i_rAt3_p0sTgRE5_1O_oUT_0f_14_pH_n3ed5_m0Re_4Cid}`
