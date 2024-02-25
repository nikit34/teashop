function localization(){
  let localizations = document.getElementsByName("language");
  let i_attr_value, lang;
  for (let i = 0; i < localizations.length; i++) {
    if (localizations[i].outerHTML.includes("selected")) {
      i_attr_value = localizations[i].outerHTML.indexOf("value=");
      lang = localizations[i].outerHTML.slice(
        i_attr_value + 7,
        i_attr_value + 9
      );
    }
  }
  return lang;
}

export { localization };