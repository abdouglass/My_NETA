# Install packages (assumed already installed)
# install.packages("ggplot2")
# install.packages("car")

# import libraries
library("ggplot2")
library("car")

# read data (Update to your location for the CSV)
data <- read.csv("/masterdictdump_final.csv")

# clean data age
data$Age <- ifelse(data$age == 0, NA, data$age)
data$Age <- ifelse(data$age >= 100, NA, data$age)

# clean winner
data$Candidates <- as.factor(recode(data$Winner, "1='Winners'; 0='Losers'"))

# clean cases for states
data$State <- as.factor(toupper(data$State))

# clean cases for affiliation
data$Affiliation <- ifelse(data$party == "ind",1,0)
data$Affiliation <- as.factor(recode(data$Affiliation, "1='Independent'; 0='Party'"))

# crimes
data$Crimes <- ifelse(data$criminal_cases > 0,ifelse(data$criminal_cases > 2,3,2),1)
data$Crimes <- as.factor(recode(data$Crimes, "1='No Case'; 2='1-2 Cases'; 3='3+ Cases'"))

# education (added on Dec 8)
data$Education_allcategories <- recode(data$EduRank, "0 = 'NA'; 1 = 'Illiterate'; 2 = 'Literate'; 3= 'Primary school'; 4 = 'Middle school'; 5= 'High school'; 6 = 'Higher secondary'; 7= 'Graduate'; 8= 'Professional grad'; 9 = 'Post graduate'; 10 = 'Doctorate'")
data$Education_allcategories <- as.factor(data$Education_allcategories)

data$Education <- as.factor(recode(data$EduRank, "0:2 = 0; 3:4 = 1; 5:6 = 2; 7:10 = 3"))
data$Education <- recode(data$Education, "0 = 'None'; 1 = 'Primary'; 2 = 'Secondary'; 3 = 'Tertiary'")

# Logit model for the entire country 
# Model with all data pooled together
logitInd <- glm(Candidates ~ Age + Education + Affiliation + Crimes, data = data, family = "binomial")

# Odds ratio
oddsInd <- exp(coef(logitInd))

# Only significant coefficients are saved in a data frame
# logitIndcoeff <- data.frame(summary(logitInd)$coef[summary(logitInd)$coef[,4] <= .05, 4])

# server
shinyServer(function(input, output) {
  
  # model equation
  
  #output$logitModel <- renderUI({
  #  withMathJax(helpText("$$P(winner = 1 | x) = \Lambda(\beta_1 + \beta_2 age + \beta_3 education  + \beta_4 party + \beta_5 cases)$$"))
  #})
  
  # output text for overview
  
  output$election_year <- renderPrint({
  
  dataState <- subset(data, State == input$State)
  #unique_years <- levels(as.factor(dataState$Year))  
  #unique_year <- levels(as.factor(data[which(data$State == input$State),]$Year))
  HTML(paste(levels(as.factor(dataState$Year))))
  
  })
  
  # output plot for age
  output$age_plot <- renderPlot({
    
    kernel <- ggplot(data = data[which(data$State == input$State),], 
                aes(x = Age))
    
    print(kernel + geom_density(aes(fill=Candidates, trim = TRUE, na.rm = TRUE), colour="white", alpha=0.5) 
          + theme(panel.grid.major=element_blank())
          + guides(fill = guide_legend(override.aes = list(colour = NULL)))
          + xlab("Age")
          )

  })
  
  # output plot for education
  output$educ_plot <- renderPlot({
  
    histogram <- ggplot(data = data[which(data$State == input$State),], 
              aes(x = EduRank, fill=Candidates))
  
    print(histogram + geom_histogram(aes(y = ..density..), 
                           colour = "white",
                           alpha=0.5,
                           position="identity",
                           binwidth = 1, freq = FALSE) 
  
        + theme(panel.grid.major=element_blank())
        + guides(fill = guide_legend(override.aes = list(colour = NULL)))
        + xlab("Highest Education")
  )
  
})

  # output plot for criminal cases
  
  output$crimes <- renderPlot({
  
  pie <- ggplot(data = data[which(data$State == input$State),], aes(x = factor(1), fill=Crimes))  
  
  print(pie + geom_bar(width = 1, position="fill",alpha=0.75,colour = "white",)
        + coord_polar(theta = "y")
        + theme(axis.text=element_blank(),axis.ticks=element_blank(),panel.grid.major=element_blank())
        + guides(fill = guide_legend(override.aes = list(colour = NULL)))
        + facet_grid(facets=.~Candidates)
  )

})

# output plot for political affiliation(none and party)

output$affiliation <- renderPlot({
  
  pie <- ggplot(data = data[which(data$State == input$State),], aes(x = factor(1), fill=Affiliation))  
  
  print(pie + geom_bar(width = 1, position="fill",alpha=0.75,colour = "white",)
        + coord_polar(theta = "y")
        + theme(axis.text=element_blank(),axis.ticks=element_blank(),panel.grid.major=element_blank())
        + guides(fill = guide_legend(override.aes = list(colour = NULL)))
        + facet_grid(facets=.~Candidates)
  )
  
})

# comparison of logit models

output$tableState = renderDataTable({
  dataState <- subset(data, State == input$State)
  # run model
  logitState <- glm(Candidates ~ Age + Education + Affiliation + Crimes, data = dataState, family = "binomial")
  # save odds ratio
  oddsState <- exp(coef(logitState))
  # format OR for state and india
  OddsRatioState <- format(round(oddsState,2))
  OddsRatioIndia <- format(round(oddsInd,2))
  # create columns
  Variable = c("Intercept", "Age" , "Primary education" , "Secondary education" , "Tertiary education" , "Party affiliation" , "More then 3 cases", "No criminal case" )
  # form data frame
  data.frame(Variable, OddsRatioState, OddsRatioIndia)
  
})

})
