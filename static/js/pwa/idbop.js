const db =
  document.location.pathname === "/feed/"
    ? "feeds-db"
    : document.location.pathname === "/"
    ? "skits-db"
      : "skt-db";
    
//Open new IndexedDB conncetion.
let storeName = db.replace("-db", "");
var dbPromise = idb.open(db, 5, function (upgradeDb) {
  upgradeDb.createObjectStore(storeName, { keyPath: "id" });
});

//collect latest post from server and store in idb.
const endpoint =
  document.location.pathname === "/feed/"
    ? "feed/"
    : document.location.pathname === "/"
    ? `?location=${document.getElementById("skitte").dataset.location}`
    : "";
fetch(`http://localhost:8000/api/skits/${endpoint}`)
  .then((res) => res.json())
  .then(function (jsondata) {
    var data = jsondata.results;
    dbPromise.then(function (db) {
      var tx = db.transaction(storeName, "readwrite");
      var feedsStore = tx.objectStore(storeName);
      for (var key in data) {
        if (data.hasOwnProperty(key)) {
          feedsStore.put(data[key]);
        }
      }
    });
  });
//retrive data from idb and display on page.
var post = "";
dbPromise
  .then(function (db) {
    var tx = db.transaction(storeName, "readonly");
    var feedsStore = tx.objectStore(storeName);
    return feedsStore.openCursor();
  })
  .then(function logItems(cursor) {
    if (!cursor) {
      //if true means we are done cursoring over all records in feeds.
      document.getElementById("offlinedata").innerHTML = post;
      return;
    }
    for (var field in cursor.value) {
      if (field == "fields") {
        feedsData = cursor.value[field];
        console.log(feedsData);
        for (var key in feedsData) {
          if (key == "content") {
            var title = "<h3>" + feedsData[key] + "</h3>";
          }
          if (key.user == "username") {
            var author = feedsData[key];
          }
          if (key == "image") {
            var body = "<p>" + feedsData[key] + "</p>";
          }
        }
        post = post + "<br>" + title + "<br>" + author + "<br>" + body + "<br>";
      }
    }
    return cursor.continue().then(logItems);
  });
