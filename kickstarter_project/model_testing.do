// DAVIS BUSTEED -- April 2019 -- ECON 388 Project
// https://github.com/dbusteed/econometrics

// get the data
use kick.dta, clear

// summary stats
sum pledged backers_count goal international days_open title_len blurb_len title_sent blurb_sent
sum cat_comics cat_crafts cat_dance cat_design cat_fashion cat_film___video cat_food cat_games cat_journalism cat_music cat_photography cat_publishing cat_technology cat_theater
sum mo_Aug mo_Dec mo_Feb mo_Jan mo_Jul mo_Jun mo_Mar mo_May mo_Nov mo_Oct mo_Sep

// log transformations, some records have pledged=0, so add 1
gen lpledged = log(pledged+1)
gen lbackers_count = log(backers_count+1)
gen lgoal = log(goal)

// simple model
reg lpledged backers_count goal international days_open

// simple model with log on goal
reg lpledged backers_count lgoal international days_open

// add in log on backers_count
reg lpledged lbackers_count lgoal international days_open

// clean out others, add in title_len
reg lpledged lbackers_count lgoal title_len

// add cat dummied
reg lpledged lbackers_count lgoal title_len cat_comics cat_crafts cat_dance cat_design cat_fashion cat_film___video cat_food cat_games cat_journalism cat_music cat_photography cat_publishing cat_technology cat_theater

// this shows a perfect corr between photo and film!
corr cat_comics cat_crafts cat_dance cat_design cat_fashion cat_film___video cat_food cat_games cat_journalism cat_photography cat_music cat_publishing cat_technology cat_theater

// same thing but with film and photo combined (BEST)
reg lpledged lbackers_count lgoal title_len cat_comics cat_crafts cat_dance cat_design cat_fashion  cat_food cat_games cat_journalism cat_music  cat_publishing cat_technology cat_theater cat_film_vid_photo

// with months
reg lpledged lbackers_count lgoal title_len mo_Aug mo_Dec mo_Feb mo_Jan mo_Jul mo_Jun mo_Mar mo_May mo_Nov mo_Oct mo_Sep

// with all dummies
reg lpledged lbackers_count lgoal title_len cat_comics cat_crafts cat_dance cat_design cat_fashion cat_food cat_games cat_journalism cat_music  cat_publishing cat_technology cat_theater cat_film_vid_photo mo_Aug mo_Dec mo_Feb mo_Jan mo_Jul mo_Jun mo_Mar mo_May mo_Nov mo_Oct mo_Sep

// check for correlation in Xs
corr lbackers_count lgoal title_len cat_comics cat_crafts cat_dance cat_design cat_fashion  cat_food cat_games cat_journalism cat_music  cat_publishing cat_technology cat_theater cat_film_vid_photo

// check significance for categories
test cat_comics= cat_crafts= cat_dance= cat_design= cat_fashion= cat_food= cat_games= cat_journalism= cat_music= cat_publishing= cat_technology= cat_theater= cat_film_vid_photo=0


// Test for heteroskedasticty
reg lpledged lbackers_count lgoal title_len cat_comics cat_crafts cat_dance cat_design cat_fashion  cat_food cat_games cat_journalism cat_music  cat_publishing cat_technology cat_theater cat_film_vid_photo
predict u, residuals
gen usq = u*u

// reg with robust SEs
reg lpledged lbackers_count lgoal title_len cat_comics cat_crafts cat_dance cat_design cat_fashion cat_food cat_games cat_journalism cat_music cat_publishing cat_technology cat_theater cat_film_vid_photo, robust
