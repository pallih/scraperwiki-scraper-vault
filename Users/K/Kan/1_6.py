require(XML)
 
hashtag <- "ows" #skouries
 
max.results <- "220" #number of results to return 100 - 1500
 
no.pages <- as.character(trunc(as.numeric(max.results)/100, digits = 1)+1)
 
tweets.df <- data.frame
 
tweets.sub.df <- data.frame
 
for(i in 1:no.pages){
     
    if (i == no.pages) {
     
        url <- paste("http://search.twitter.com/search.rss?q=%23",hashtag,"&rpp=",as.character(as.numeric(max.results)%%100),"&page=",i,"&include_entities=true&result_type=mixed", sep="")
         
        }
     
    else {
     
        url <- paste("http://search.twitter.com/search.rss?q=%23",hashtag,"&rpp=",100,"&page=",i,"&include_entities=true&result_type=mixed", sep="")
     
        }
     
    doc <- xmlTreeParse(url,useInternal=T)
 
    author <- xpathSApply(doc, "//item//author", xmlValue)
 
    tweet <- xpathSApply(doc, "//item//title", xmlValue)
  
    pubDate <- xpathSApply(doc, "//item//pubDate", xmlValue)
 
    tweets.sub.df <- cbind(pubDate,tweet,author)
     
    if (i == 1) { tweets.df <- tweets.sub.df } else { tweets.df <- rbind(tweets.df,tweets.sub.df) }
     
    } 
     
write.csv(tweets.df,"tweets.csv")