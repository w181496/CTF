# Netcorp

這題打開來是一個啥東西都沒的近態頁面

簡單戳一下讓他噴錯，會發現是 Tomcat

立馬掃一下 port

果然有開 8009 port

直接戳戳看 ghostcat 洞

成功讀到 web.xml:

```
<!DOCTYPE web-app PUBLIC
 "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
 "http://java.sun.com/dtd/web-app_2_3.dtd" >

<web-app>
  <display-name>NetCorp</display-name>


  <servlet>
      <servlet-name>ServeScreenshot</servlet-name>
      <display-name>ServeScreenshot</display-name>
      <servlet-class>ru.volgactf.netcorp.ServeScreenshotServlet</servlet-class>
  </servlet>

  <servlet-mapping>
      <servlet-name>ServeScreenshot</servlet-name>
      <url-pattern>/ServeScreenshot</url-pattern>
  </servlet-mapping>


    <servlet>
        <servlet-name>ServeComplaint</servlet-name>
        <display-name>ServeComplaint</display-name>
        <description>Complaint info</description>
        <servlet-class>ru.volgactf.netcorp.ServeComplaintServlet</servlet-class>
    </servlet>

    <servlet-mapping>
        <servlet-name>ServeComplaint</servlet-name>
        <url-pattern>/ServeComplaint</url-pattern>
    </servlet-mapping>

    <error-page>
        <error-code>404</error-code>
        <location>/404.html</location>
    </error-page>



</web-app>
```

接著把那兩個 servlet 下載下來

其中 ServeScreenshotServlet.class 反編譯之後如下:

```
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.math.BigInteger;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.annotation.MultipartConfig;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Part;
import ru.volgactf.netcorp.ServeScreenshotServlet;

@MultipartConfig
public class ServeScreenshotServlet extends HttpServlet {
  private static final String SAVE_DIR = "uploads";

  public ServeScreenshotServlet() {
    System.out.println("ServeScreenshotServlet Constructor called!");
  }

  public void init(ServletConfig config) throws ServletException {
    System.out.println("ServeScreenshotServlet \"Init\" method called");
  }

  public void destroy() {
    System.out.println("ServeScreenshotServlet \"Destroy\" method called");
  }

  protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    String appPath = request.getServletContext().getRealPath("");
    String savePath = appPath + "uploads";
    File fileSaveDir = new File(savePath);
    if (!fileSaveDir.exists())
      fileSaveDir.mkdir(); 
    String submut = request.getParameter("submit");
    if (submut == null || !submut.equals("true"));
    for (Part part : request.getParts()) {
      String fileName = extractFileName(part);
      fileName = (new File(fileName)).getName();
      String hashedFileName = generateFileName(fileName);
      String path = savePath + File.separator + hashedFileName;
      if (path.equals("Error"))
        continue; 
      part.write(path);
    } 
    PrintWriter out = response.getWriter();
    response.setContentType("application/json");
    response.setCharacterEncoding("UTF-8");
    out.print(String.format("{'success':'%s'}", new Object[] { "true" }));
    out.flush();
  }

  private String generateFileName(String fileName) {
    try {
      MessageDigest md = MessageDigest.getInstance("MD5");
      md.update(fileName.getBytes());
      byte[] digest = md.digest();
      String s2 = (new BigInteger(1, digest)).toString(16);
      StringBuilder sb = new StringBuilder(32);
      for (int i = 0, count = 32 - s2.length(); i < count; i++)
        sb.append("0"); 
      return sb.append(s2).toString();
    } catch (NoSuchAlgorithmException e) {
      e.printStackTrace();
      return "Error";
    } 
  }

  private String extractFileName(Part part) {
    String contentDisp = part.getHeader("content-disposition");
    String[] items = contentDisp.split(";");
    for (String s : items) {
      if (s.trim().startsWith("filename"))
        return s.substring(s.indexOf("=") + 2, s.length() - 1); 
    } 
    return "";
  }
}
```

這邊我們能直接上傳一個任意內容的檔案

所以我們直接傳一個 jsp webshell

接著再用 ghostcat 去 eval 我們傳的這個 webshell 就能 RCE


