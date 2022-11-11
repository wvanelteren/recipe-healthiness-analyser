# #### SETUP RECIPES DATA ####
#
# install.packages("ggplot2")
# install.packages("moments")
# install.packages("dplyr")
# install.packages("lmerTest")
# install.packages("nlme")
# install.packages("lme4")
# install.packages("psycho")
# install.packages("broom")
# install.packages("sjPlot")
# install.packages("tidyverse")
# install.packages("report")
# install.packages("effects")
# install.packages("rstatix")
# install.packages("robustlmm")
# install.packages("effects")
# install.packages("ggeffects")
# install.packages("stargazer")
# install.packages("gmodels")
# install.packages("car")
library(rstatix)
library(moments)
library(ggplot2)
library(dplyr)
library(lmerTest)
library(nlme)
library(lme4)
library(psycho)
library(broom)
library(knitr)
library(sjPlot)
library(effects)
library(report)
library(effects)
library(gmodels)
library(car)

# Import Recipes Dataset
recipes <- read.csv(file='analysed_recipes.csv')
names(recipes)

# Set variables
influencer <- recipes$influencer
likes <- recipes$likes
comments <- recipes$comments
media <- recipes$Media
nutri_score <- recipes$nutri_score
nutri_score_label <- recipes$nutri_score_label
saturated_fat <- recipes$nutri_saturated_fat.g.
calories <- recipes$nutri_calories.kj.

recipes_optimized <- subset(recipes, !likes %in% identify_outliers(recipes, "likes")$likes)
recipes_optimized <- subset(recipes_optimized_2, !comments %in% identify_outliers(recipes_optimized_2, "comments")$comments)
skewness(recipes_optimized$likes)
likes_o_log <- log10(recipes_optimized$likes)
comments_o_sqrt <- sqrt(recipes_optimized$comments)

influencer_o <- recipes_optimized$influencer
likes_o <- recipes_optimized$likes
comments_o <- recipes_optimized$comments
media_o <- recipes_optimized$Media
nutri_score_o <- recipes_optimized$nutri_score
nutri_score_label_o <- recipes_optimized$nutri_score_label
saturated_fat_o <- recipes_optimized$saturated_fat.g.

# Descriptive stats for followers, likes and comments
followers <- recipes %>% distinct(followers)
followers <- followers$followers
stat.desc(followers)
tab1(recipes$Media, sort.group = "descending", cum_percent = TRUE)
stat.desc(likes)
stat.desc(comments)

#### Distribution healthiness recipes ####

# Calculate distribution of nutri_score
var(nutri_score)
sd(nutri_score)

#normalize healthiness score distribution
nutri_score_cube <- (nutri_score+1-min(nutri_score))

# Anova to check if healthiness score is sign different per influencers
group_nutri_score <- lm(nutri_score_cube ~ influencer, data = recipes)
anova(group_nutri_score) # Significantly Different

# Calculate distribution of nutri_score_label
nutri_label_1 <- recipes %>%
  group_by(nutri_score_label) %>%
  summarise(cnt = n()) %>%
  mutate(freq = round(cnt / sum(cnt), 3)) %>%
  arrange(desc(freq))
head(as.data.frame(nutri_label_1))

# Calculate distribution of nutri_score_label per influencer
nutri_label_2 <- recipes %>%
  group_by(nutri_score_label, influencer) %>%
  summarise(cnt = n()) %>%
  mutate(freq = round(cnt / sum(cnt), 3)) %>%
  arrange(desc(freq))
attach(nutri_label_2)

table(nutri_label_2$influencer, nutri_label_2$count)


# Nutri Score Label distribution, as classified A/B = Healthy, D/E = Unhealthy

nutri_label_3 <- recipes %>%
  mutate(nutri_score_H = case_when(
    (nutri_score_label == "A") ~ "A/B",
    (nutri_score_label == "B") ~ "A/B",
    (nutri_score_label == "C") ~ "C",
    (nutri_score_label == "D") ~ "D/E",
    (nutri_score_label == "E") ~ "D/E",
  )) %>%
  group_by(nutri_score_H) %>%
  summarise(cnt = n()) %>%
  mutate(freq = round(cnt / sum(cnt), 3)) %>%
  arrange(desc(freq))
head(as.data.frame(nutri_label_3))

# Calculate percentage of nutri_score label that is not A or B per influencer

nutri_label_4 <- recipes %>%
  mutate(nutri_score_H = case_when(
    (nutri_score_label == "A") ~ "A/B",
    (nutri_score_label == "B") ~ "A/B",
    (nutri_score_label == "C") ~ "C",
    (nutri_score_label == "D") ~ "D/E",
    (nutri_score_label == "E") ~ "D/E",
  )) %>%
  group_by(influencer, nutri_score_H) %>%
  summarise(cnt = n()) %>%
  mutate(freq = round(cnt / sum(cnt), 3)) %>%
  arrange(desc(freq))


### Visualize Distribution ###

# Add nutri_score_label colour

A_c <- "#00823F"
B_c <- "#86BC2B"
C_c <- "#FECC00"
D_c <- "#EE8200"
E_c <- "#E73C09"

colors_legend <- c("A" = A_c, "B" = B_c, "C" = C_c, "D" = D_c, E = E_c)

# visualise distribution nutri_score

ggplot(recipes, aes(x="Nutri-Score", y=nutri_score)) +
  geom_boxplot()+
  coord_flip() +
  annotate("rect",
           xmin = -Inf, xmax = Inf,
           ymin = c(-10, -1, 2, 10, 18), ymax = c(-1, 2, 10, 18, 24), alpha = .4,
           fill = c(A_c, B_c, C_c, D_c, E_c))


# Create horizontal boxplot
nutri_score_distribution <- ggplot(recipes,
                                   aes(x = influencer, y = nutri_score)) +
  geom_boxplot() +
  coord_flip()


nutri_score_distribution <- nutri_score_distribution + annotate("rect",
                                                                xmin = -Inf, xmax = Inf,
                                                                ymin = c(-10, -1, 2, 10, 18), ymax = c(-1, 2, 10, 18, 24), alpha = .4,
                                                                fill = c(A_c, B_c, C_c, D_c, E_c))

nutri_score_distribution

# Add legend
nutri_score_distribution + scale_fill_manual(name = 'Nutri-Score',
                                             values = c(A_c, B_c, C_c, D_c, E_c))


# Add Legend:
# Label A: Dark Green
# Label B: Green
# Label C: Yellow
# Label D: Red
# Label E: Dark Red

# visualise diverging
nutri_score_inf.mean <- recipes %>%
  group_by(influencer) %>%
  summarise_at(vars(nutri_score), list(mean = mean))

nutri_score_inf.mean$mean <- round(nutri_score_inf.mean$mean, 1)

nutri_score_inf.mean <- nutri_score_inf.mean %>%
  mutate(nutri_score_label = case_when(
    (between(mean, -7, -1)) ~ "A",
    (between(mean, -1, 2)) ~ "B",
    (between(mean, 2, 10)) ~ "C"))

ggplot(nutri_score_inf.mean2, aes(x=reorder(influencer, mean), y=mean, label=mean)) +
  geom_point(stat='identity', shape = 1, size = 10, color="black")  +
  annotate("rect",
           xmin = -Inf, xmax = Inf,
           ymin = c(-6, -1, 2), ymax = c(-1, 2, 6), alpha = .4,
           fill = c(A_c, B_c, C_c)) +
  scale_color_manual(name = "mean Nutri-Score",
                     label = "Mean Nutri_score",
                     values = mean) +
  geom_text(color = "black", size = 3) +
  labs(title="Mean Nutri-Score per Influencer",
       x = "",
       y = "Nutri-Score") +
  ylim(-6, 6) +
  coord_flip()


#### Interaction healthiness sore and likes/comments ####

#explore distribution of response variables
hist(likes)
hist(comments)

# Calculate skewness
skewness(likes_o)
skewness(comments_o)
skewness(likes)
skewness(comments)

# Data of response variables is heavily skewed
# Log transfer + sqrt transfer
likes_log <- log10(likes)
likes_o_log <- log10(likes_o)
comments_sqrt <- sqrt(comments)
comments_o_sqrt <- sqrt(comments_o)

skewness(likes_log)
skewness(comments_sqrt)
skewness(likes_o_log)
skewness(comments_o_sqrt

         # Data is now approximately symmetric for both response variables!

         # Standardize response variable
         nutri_score_scaled <- scale(nutri_score, center = TRUE, scale = TRUE)
         nutri_score_o_scaled <- scale(nutri_score_o, center = TRUE, scale = TRUE)

         # Mixed effect model nutri_score -> likes, random intercept for influencer
         lmer_likes <- lmer(likes_log ~ nutri_score + (1+nutri_score|influencer), data = recipes)
         lmer_likes5 <- lmer(likes_log ~ nutri_score + (1|influencer), data = recipes)
         summary(lmer_likes, ddf="Kenward-Roger")
         anova(lmer_likes, lmer_likes5)
         report(lmer_likes5)

         # Mixed effect model nutri_score -> comments, random intercept for influencer
         lmer_comments <- lmer(comments_sqrt ~ nutri_score + (1|influencer:media), data = recipes)
         summary(lmer_comments, ddf="Kenward-Roger")

         # MEM for optimized data
         lmer_likes_o <- lmer(likes_o_log ~ nutri_score_o + (1|influencer_o), data = recipes_optimized)
         summary(lmer_likes_o)
         lmer_comments_o <- lmer(comments_o_sqrt ~ nutri_score_o + (1|influencer_o), data = recipes_optimized)
         summary(lmer_comments_o)

         # Check plots to see if none of the mix effect model assumptions are violated

         # Likes
         qqnorm(resid(lmer_likes))
         qqline(resid(lmer_likes))
         qqnorm(resid(lmer_likes_o))
         qqline(resid(lmer_likes_o))

         plot(lmer_likes_o)
         plot(lmer_likes)
         plot_model(lmer_likes, type = "diag")
         plot_model(lmer_likes_o, type = "diag")

         # Comments
         qqnorm(resid(lmer_comments))
         qqline(resid(lmer_comments))
         qqnorm(resid(lmer_comments_o))
         qqline(resid(lmer_comments_o))

         plot_model(lmer_comments, type = "diag")
         plot_model(lmer_comments_o, type = "diag")

         # No assumption violations!!!!

         # get p values
         tab_model(lmer_likes)
         tab_model(lmer_likes_o)
         tab_model(lmer_comments)
         tab_model(lmer_comments_o)

         # Time for a new model, lets control for type of media #
         lmer_likes_2 <- lmer(likes_log ~ nutri_score_scaled + (1|influencer), data = recipes)
         tab_model(lmer_likes_2)
         report(lmer_likes_2)

         lmer_comments_2 <- lmer(comments_sqrt ~ nutri_score_scaled + media + (1|influencer), data = recipes)
         lmer_likes_o_2 <- lmer(likes_o_log ~ nutri_score_o + media_o + (1|influencer_o), data = recipes_optimized)
         lmer_comments_o_2 <- lmer(comments_o_sqrt ~ nutri_score_o + media_o + (1|influencer_o), data = recipes_optimized)
         lmer_likes_c_2 <- lmer(likes_log ~ calories + media + (1|influencer), data = recipes)
         lmer_comments_c_2 <- lmer(comments_sqrt ~ calories + media + (1|influencer), data = recipes)
         lmer_likes_oc_2 <- lmer(likes_oc_log ~ calories_oc + media_oc + (1|influencer_oc), data = recipes_optimized_c)
         lmer_comments_oc_2 <- lmer(comments_oc_sqrt ~ calories_oc + media_oc + (1|influencer_oc), data = recipes_optimized_c)
         lmer_likes_f_2 <- lmer(likes_log ~ saturated_fat + media + (1|influencer), data = recipes)
         lmer_comments_f_2 <- lmer(comments_sqrt ~ saturated_fat + media + (1|influencer), data = recipes)
         lmer_likes_of_2 <- lmer(likes_of_log ~ saturated_fat_of + media_of + (1|influencer_of), data = recipes_optimized_f)
         lmer_comments_of_2 <- lmer(comments_of_sqrt ~ saturated_fat_of + media_of + (1|influencer_of), data = recipes_optimized_f)

         tab_model(lmer_likes_2)       # p = 0.8
         tab_model(lmer_likes_o_2)     # p = 0.5
         tab_model(lmer_comments_2)    # p = 0.6
         tab_model(lmer_comments_o_2)  # p = 0.3

         # Test for better model via likelihood ratio test
         anova(lmer_likes_2, lmer_likes)
         anova(lmer_likes_o_2, lmer_likes_o)
         anova(lmer_comments_2, lmer_comments)     # lmer_comments_2 sig better
         anova(lmer_comments_o_2, lmer_comments_o) # lmer_comments_o_2 sig better

         # Introducing random slopes
         lmer_likes_3 <- lmer(likes_log ~ nutri_score_scaled + media + (1+1|influencer), data = recipes)
         lmer_comments_3 <- lmer(comments_sqrt ~ nutri_score_scaled + media + (1+1|influencer), data = recipes)
         lmer_likes_o_3 <- lmer(likes_o_log ~ nutri_score_o_scaled + media_o + (1+1|influencer), data = recipes_optimized)
         lmer_comments_o_3 <- lmer(comments_o_sqrt ~ nutri_score_o_scaled + media_o + (1+1|influencer), data = recipes_optimized)

         tab_model(lmer_likes_3)       # p = 0.8
         tab_model(lmer_likes_o_3)     # p = 0.5
         tab_model(lmer_comments_3)    # p = 0.6
         tab_model(lmer_comments_o_3)  # p = 0.3

         # Nutri_score, saturated fat and calories do not significantly predict amounts of likes or comments