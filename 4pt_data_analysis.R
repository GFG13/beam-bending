####################################################################
#  required libraries
####################################################################

library(readxl)
library(sp)
library(gstat)
####################################################################
#  DATA IMPORT  
####################################################################
file_name <- "/data/sig_t-output.xlsx"

dat <- read_excel(paste0(temp_path,file_name), na="")
dat_G_INT <- subset(dat, break_type == "INT" | break_type == "INT*")
dat_G_MID <- subset(dat, break_type == "MID")

x <- dat$temp_degC
y <- dat$peak_stressMPa

x1 <- dat_G_INT$temp_degC
y1 <- dat_G_INT$peak_stressMPa
x2 <- dat_G_MID$temp_degC
y2 <- dat_G_MID$peak_stressMPa

####################################################################
#  LINEAR LEAST SQUARES REGRESSION  
####################################################################
fit <- lm(y ~ 0 + x - 1)
summary(fit)
confint(fit)

x_new <- data.frame(x=seq(min(x), max(x), length=20))
pred_int <- predict(fit, x_new  , interval='predict')
conf_int <- predict(fit, x_new  , interval='confidence')

####################################################################
#  PLOT 1 SETTINGS
####################################################################
# plot maxima
ymin <- 0; ymax <- 3.5; yint <- .5
xmin <- -30; xmax <- 0; xint <- 5
dummy.x <- seq(xmin,xmax,length=50)

# line widths: pixels to mm
lw18  <-  432/635; lw25 <-  120/127; lw35 <-  168/127
lw50  <-  240/127; lw71 <-  1704/635; lw1 <-  480/127
lw1.4 <-  672/127; lw2  <-  960/127

# plot size
w.cm = 8.5; h.cm = w.cm * 3/4
w.in = w.cm/2.54 ; h.in = h.cm/2.54

# plot space
svg('T_sigma.svg', pointsize=8, width=w.in, height=h.in)
mypar <- par(pty='m', mar=c(2,2.5,0.25,0.1)+0.1, cex=1, lend=2, lwd=lw18, xpd = F)

plot(NA, xlim=c(xmin, xmax), ylim=c(ymin,ymax), xlab='', ylab='', axes=F)
points(x1, y1, pch=4, cex=0.8, col = "black")
points(x2, y2, pch=3, cex=0.8, col = "darkgray")
#lines(dummy.x, predict(fit, data.frame(x=dummy.x)), col="red", lty = 2)
#lines(dummy.x, predict(fit2, data.frame(x=dummy.x)), col="blue", lty = 2)
matlines(x_new, conf_int, col=2, lty=c(1,2,2),lwd = lw18)  
matlines(x_new, pred_int, col=2, lty=c(1,4,4),lwd = lw18)

# Horizonal axis
axis(1, pos=ymin, labels=NA, lwd=lw18, tck=-0.01, at = seq(xmin,xmax,xint/2))
axis(1, lwd=0, line=-1, las=1,at = seq(xmin,xmax,xint))
mtext(expression('Temperature ('*degree*'C)',sep=""), side=1, line=1, font=1)

# Vertical axis
axis(2, pos=xmin, labels=NA, lwd=lw18, tck=-0.01,at = seq(ymin,ymax,yint/2))
axis(2, lwd=0, line=-1.25, las=1)
mtext('Stress magnitude (MPa)', side=2, line=1.25, font=1)
axis(3, pos=ymax, tck=0.0, labels=NA, lwd=lw18)
axis(4, pos=xmax, tck=0.0, labels=NA,  lwd=lw18)

box(which = 'outer', lty = 'solid', col='gray')
par(mypar)

dev.off()
####################################################################


#plot(dat$temp_degC,dat$peak_stressMPa)
# 
# 
# 
# mypar2 <- par(pty='m', mfrow=c(2,2),cex=1, lend=2, lwd=lw18)
# plot(fit)
# par(mypar2)
# dev.off()

