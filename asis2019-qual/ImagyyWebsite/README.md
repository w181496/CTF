# Imagyy website

這題是用React寫的

主要邏輯在這: http://37.139.17.29:5000/static/js/main.7489cd39.chunk.js

```javascript
(window.webpackJsonp = window.webpackJsonp || []).push([
    [0], {
        136: function(e, t, a) {},
        137: function(e, t, a) {
            "use strict";
            a.r(t);
            var n = a(0),
                r = a.n(n),
                c = a(59),
                l = a.n(c),
                i = a(5),
                s = a(6),
                u = a(8),
                o = a(7),
                h = a(9),
                m = a(23),
                f = a(22),
                d = function(e) {
                    function t() {
                        return Object(i.a)(this, t), Object(u.a)(this, Object(o.a)(t).apply(this, arguments))
                    }
                    return Object(h.a)(t, e), Object(s.a)(t, [{
                        key: "render",
                        value: function() {
                            return r.a.createElement("div", null, r.a.createElement("h2", null, "HELLO"), r.a.createElement("p", null, "This is imagyy main site. This site doesn't have online registration."))
                        }
                    }]), t
                }(n.Component),
                b = function(e) {
                    function t() {
                        return Object(i.a)(this, t), Object(u.a)(this, Object(o.a)(t).apply(this, arguments))
                    }
                    return Object(h.a)(t, e), Object(s.a)(t, [{
                        key: "render",
                        value: function() {
                            return r.a.createElement("div", null, r.a.createElement("h2", null, "STUFF"), r.a.createElement("p", null, "The stuff goes here, under construction."))
                        }
                    }]), t
                }(n.Component),
                p = function(e) {
                    function t() {
                        return Object(i.a)(this, t), Object(u.a)(this, Object(o.a)(t).apply(this, arguments))
                    }
                    return Object(h.a)(t, e), Object(s.a)(t, [{
                        key: "render",
                        value: function() {
                            return r.a.createElement("div", null, r.a.createElement("h2", null, "GOT QUESTIONS?"), r.a.createElement("p", null, "The easiest thing to do is post on our ", r.a.createElement("a", {
                                href: "http://google.com"
                            }, "website"), "."))
                        }
                    }]), t
                }(n.Component),
                O = a(31),
                v = a(26),
                j = a(142),
                g = a(139),
                E = a(141),
                k = a(140),
                y = (a(73), a(21)),
                L = a.n(y),
                S = a(18),
                R = S.a.getURLs().authBaseURL,
                U = function(e) {
                    function t(e) {
                        var a;
                        return Object(i.a)(this, t), (a = Object(u.a)(this, Object(o.a)(t).call(this, e))).handleChange = function(e) {
                            a.setState(Object(O.a)({}, e.target.id, e.target.value))
                        }, a.handleSubmit = function(e) {
                            e.preventDefault()
                        }, a.handleClick = function() {
                            var e = {
                                    userid: a.state.username,
                                    password: a.state.password
                                },
                                t = Object(v.a)(Object(v.a)(a));
                            L.a.post(R + "login", e).then(function(e) {
                                "1" === JSON.parse(e.data).result.data ? (alert("Login successfull"), t.setState({
                                    fireRedirect: !0
                                })) : alert("Login failed due to invalid credentials.")
                            }).catch(function(e) {
                                console.log(e)
                            })
                        }, a.state = {
                            username: "",
                            password: ""
                        }, a
                    }
                    return Object(h.a)(t, e), Object(s.a)(t, [{
                        key: "validateForm",
                        value: function() {
                            return this.state.username.length > 0 && this.state.password.length > 0
                        }
                    }, {
                        key: "render",
                        value: function() {
                            var e = this,
                                t = this.state.fireRedirect;
                            return r.a.createElement("div", {
                                className: "Login"
                            }, r.a.createElement("form", {
                                onSubmit: this.handleSubmit
                            }, r.a.createElement(j.a, {
                                controlId: "username",
                                bsSize: "large"
                            }, r.a.createElement(g.a, null, "Username"), r.a.createElement(E.a, {
                                autoFocus: !0,
                                type: "text",
                                value: this.state.username,
                                onChange: this.handleChange
                            })), r.a.createElement(j.a, {
                                controlId: "password",
                                bsSize: "large"
                            }, r.a.createElement(g.a, null, "Password"), r.a.createElement(E.a, {
                                value: this.state.password,
                                onChange: this.handleChange,
                                type: "password"
                            })), r.a.createElement(k.a, {
                                block: !0,
                                bsSize: "large",
                                disabled: !this.validateForm(),
                                type: "submit",
                                onClick: function(t) {
                                    return e.handleClick(t)
                                }
                            }, "Login")), t && r.a.createElement(f.a, {
                                to: "/user_panel"
                            }))
                        }
                    }]), t
                }(n.Component),
                C = a(67),
                w = S.a.getURLs().configBaseURL,
                _ = S.a.getURLs().panelBaseURL,
                T = function(e) {
                    function t(e) {
                        var a;
                        return Object(i.a)(this, t), (a = Object(u.a)(this, Object(o.a)(t).call(this, e))).state = {
                            data: {},
                            token: null
                        }, a
                    }
                    return Object(h.a)(t, e), Object(s.a)(t, [{
                        key: "getData",
                        value: function() {
                            return {
                                authToken: this.state.authToken,
                                user_ID: this.state.user_ID
                            }
                        }
                    }, {
                        key: "refresh_token",
                        value: function() {
                            var e = this;
                            L.a.get(w + "refresh_token").then(function(t) {
                                e.setState({
                                    token: JSON.parse(t.data).result.data.token
                                })
                            }).catch(function(e) {
                                console.log(e)
                            })
                        }
                    }, {
                        key: "privateInfo",
                        value: function() {
                            var e = {
                                user_id: this.state.user_ID
                            };
                            L.a.post(_ + "get_user_information.json", e, {
                                headers: {
                                    authToken: this.state.token
                                }
                            }).then(function(e) {}).catch(function(e) {
                                console.log(e)
                            })
                        }
                    }, {
                        key: "render",
                        value: function() {
                            return r.a.createElement("div", {
                                className: "user_info"
                            }, r.a.createElement("input", {
                                type: "hidden",
                                value: this.state.authToken
                            }), r.a.createElement("input", {
                                type: "hidden",
                                value: this.state.user_ID
                            }))
                        }
                    }]), t
                }(n.Component),
                I = S.a.getURLs().panelBaseURL,
                N = function(e) {
                    function t(e) {
                        var a;
                        return Object(i.a)(this, t), (a = Object(u.a)(this, Object(o.a)(t).call(this, e))).handleSubmit = function(e) {
                            e.preventDefault()
                        }, a.state = {
                            user_data: {}
                        }, a
                    }
                    return Object(h.a)(t, e), Object(s.a)(t, [{
                        key: "componentDidMount",
                        value: function() {
                            var e = this;
                            L.a.get(I + "user.json").then(function(t) {
                                "200" === t.status && e.setState({
                                    user_data: JSON.parse(t.data)
                                })
                            }).catch(function(e) {
                                console.log(e)
                            })
                        }
                    }, {
                        key: "render",
                        value: function() {
                            return r.a.createElement("div", {
                                className: "Panel"
                            }, this.state && this.state.user_data && r.a.createElement("div", null, JSON.stringify(this.state.user_data)), r.a.createElement(T, null), r.a.createElement(C.a, null))
                        }
                    }]), t
                }(n.Component),
                B = (a(136), function(e) {
                    function t() {
                        return Object(i.a)(this, t), Object(u.a)(this, Object(o.a)(t).apply(this, arguments))
                    }
                    return Object(h.a)(t, e), Object(s.a)(t, [{
                        key: "render",
                        value: function() {
                            return r.a.createElement(m.a, null, r.a.createElement("div", null, r.a.createElement("h1", null, "Imagyy Main Site"), r.a.createElement("ul", {
                                className: "header"
                            }, r.a.createElement("li", null, r.a.createElement(m.b, {
                                exact: !0,
                                to: "/",
                                class: "active"
                            }, "Home")), r.a.createElement("li", null, r.a.createElement(m.b, {
                                to: "/stuff"
                            }, "Stuff")), r.a.createElement("li", null, r.a.createElement(m.b, {
                                to: "/contact"
                            }, "Contact")), r.a.createElement("li", null, r.a.createElement(m.b, {
                                to: "/login"
                            }, "Log-in"))), r.a.createElement("div", {
                                className: "content"
                            }, r.a.createElement(f.b, {
                                exact: !0,
                                path: "/",
                                component: d
                            }), r.a.createElement(f.b, {
                                path: "/stuff",
                                component: b
                            }), r.a.createElement(f.b, {
                                path: "/contact",
                                component: p
                            }), r.a.createElement(f.b, {
                                path: "/login",
                                component: U
                            }), r.a.createElement(f.b, {
                                path: "/panel",
                                component: N
                            }))))
                        }
                    }]), t
                }(n.Component));
            l.a.render(r.a.createElement(B, null), document.getElementById("root"))
        },
        18: function(e, t, a) {
            "use strict";
            a.d(t, "a", function() {
                return u
            });
            var n = a(5),
                r = a(6),
                c = a(8),
                l = a(7),
                i = a(9),
                s = a(0),
                u = function(e) {
                    function t() {
                        return Object(n.a)(this, t), Object(c.a)(this, Object(l.a)(t).apply(this, arguments))
                    }
                    return Object(i.a)(t, e), Object(r.a)(t, null, [{
                        key: "getURLs",
                        value: function() {
                            var e = "http://37.139.17.29:8080/";
                            return {
                                redirectURL: e + "r/self/",
                                authBaseURL: e + "backend/auth/",
                                panelBaseURL: e + "backend/panel/",
                                configBaseURL: e + "backend/config/"
                            }
                        }
                    }]), t
                }(s.Component)
        },
        67: function(e, t, a) {
            "use strict";
            (function(e) {
                a.d(t, "a", function() {
                    return h
                });
                var n = a(31),
                    r = a(5),
                    c = a(6),
                    l = a(8),
                    i = a(7),
                    s = a(9),
                    u = a(0),
                    o = a(18).a.getURLs().redirectURL,
                    h = function(t) {
                        function a(t) {
                            var c;
                            return Object(r.a)(this, a), (c = Object(l.a)(this, Object(i.a)(a).call(this, t))).handleChange = function(e) {
                                c.setState(Object(n.a)({}, e.target.id, e.target.value))
                            }, c.handleRedirect = function() {
                                var t = new e(c.state.URL).toString("base64");
                                window.location.href = o + "/" + t
                            }, c.handleSubmit = function(e) {
                                e.preventDefault()
                            }, c.state = {
                                URL: ""
                            }, c
                        }
                        return Object(s.a)(a, t), Object(c.a)(a, [{
                            key: "render",
                            value: function() {
                                return null
                            }
                        }]), a
                    }(u.Component)
            }).call(this, a(132).Buffer)
        },
        68: function(e, t, a) {
            e.exports = a(137)
        },
        73: function(e, t, a) {}
    },
    [
        [68, 1, 2]
    ]
]);
//# sourceMappingURL=main.7489cd39.chunk.js.map
```

從裡頭可以找到幾個endpoint:

- configBaseURL: `backend/config/`
- redirectURL: `r/self/`
- authBaseURL: `backend/auth/`
- panelBaseURL: `backend/panel/`
- `/user_panel`
- `/panel`
- ...

其中`/backend/config/refresh_token`，可以去要一組token

這組token可以用在`/backend/panel/get_user_information.json`

這個`get_user_information.json`可以拿來查指定使用者的資料

e.g. POST `{"user_id": xxx}`，並附帶`authToken` header

然後只要查`user_id`為1的user就會噴FLAG了


