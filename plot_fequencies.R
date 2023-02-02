setwd("/home/betti/culturalDataScience")
data<-read.csv("/home/betti/culturalDataScience/frequency_without_linking/entity_freq_29_1.csv")

library(ggstream)
library(ggplot2)
library(dplyr)
library(EnvStats)

sum_freq <- summarise(group_by(subset.data.frame(data, select = -c(book, year)), name), fre_sum = sum(frequency))
sum_freq_sort <- sum_freq[order(sum_freq$fre_sum, decreasing = TRUE), ]
sum_freq_sort_sub <- subset.data.frame(sum_freq_sort, fre_sum > 10 & !(name %in% filter_out), select = name)

data_filtered <- left_join(sum_freq_sort_sub, data)


get_outlier_rosner <- function(data_composer){
  test <- rosnerTest(data_composer$frequency, k=2)
  return(test)
}

4
plot_data <- function(data){
  ggplot(data, aes(x = year, y = frequency, fill = name)) +
    geom_stream() +
    geom_stream_label(aes(label = name))
}

outliers <- matrix()

for (composer in group_data(group_by(data_filtered, name)))
  outlier <- get_outlier_rosner(composer)
  View(outlier)
  
  
  