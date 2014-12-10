#assume libraries are already installed

library(ggplot2)

# read data (update to the location of your csv
 dataWB <- read.csv(WB_data.csv",header=FALSE)

shinyUI(fluidPage(
  
  # Application title
  titlePanel("Political Selection in the World's Largest Democracy"),
  
  # Sidebar panel
  sidebarLayout(
    sidebarPanel(
 
      # Sidebar with a drop down input for state
      selectInput(inputId = "State",
                  label = "Please select a state",
                  choices = levels(data$State),
                  selected = "GOA",
                  selectize=TRUE
                  ),
      
      hr(),
      h5("Average Income & Education Level in India in 2010"),
      p(dataWB$V1[1],": US$",dataWB$V3[1], style = "font-size:12px"),
      p(dataWB$V1[2],": ",format(round(dataWB$V3[2]*100,2), nsmall=2),"%", style = "font-size:12px"),
      p(dataWB$V1[3],": ",format(round(dataWB$V3[3]*100,2), nsmall=2),"%", style = "font-size:12px"),
      p(dataWB$V1[4],": ",format(round(dataWB$V3[4]*100,2), nsmall=2),"%", style = "font-size:12px"),
      p(dataWB$V1[5],": ",format(round(dataWB$V3[5]*100,2), nsmall=2),"%", style = "font-size:12px"),
      hr(),
      h5("Logistic Model"),
      withMathJax(),
      p("$$P(winner = 1|x) = \\lambda(\\beta_1+\\beta_2Age$$",style = "font-size:12px"),
      p("$$+\\beta_3Education+\\beta_4Party +\\beta_5Cases)$$",style = "font-size:12px"),
      hr()

), 

    # Main panel
    mainPanel(
      h4("Overview"),
      p("Number of election years:", levels(as.factor(data$Year)),style = "font-size:12px"),
      p("Number of observations:", nrow(data),style = "font-size:12px"),
      h4("Distribution of Age"),
      plotOutput(outputId = "age_plot", width = "600px", height = "300px"),
      h4("Distribution of Highest Education"),
      plotOutput(outputId = "educ_plot", width = "600px", height = "300px"),
      h4("Distribution of Criminal Cases"),
      plotOutput(outputId = "crimes", width = "600px", height = "300px"),
      h4("Distribution of Political Affiliation"),
      plotOutput(outputId = "affiliation", width = "600px", height = "300px"),
      h4("What are the odds of winning an election?"),
      dataTableOutput(outputId = "tableState")
        
)

)

))
