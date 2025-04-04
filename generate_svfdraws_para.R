# ------------------------------------------------------------------------
# 优化后的并行版本（修正维度问题及环境初始化问题）
# ------------------------------------------------------------------------
rm(list=ls())  # 只保留一次环境清理
sink("NUL")        # Windows
options(warn = -1)
suppressPackageStartupMessages({
  library(coda)
  library(stochvol)
  library(foreach)
  library(doParallel)
  library(parallel)
  library(iterators)
})

options(digits=17)
# 数据加载和初始化 --------------------------------------------------------
set.seed(11000) # for replication
vt <- read.table('vft.txt', sep = '\t')
T <- dim(vt)[1]
N <- dim(vt)[2]

# 数据预处理
for (i in 1:N) {
  if (min(log(vt[,i]^2)) == -Inf) {
    vt[,i] <- vt[,i] + 0.00001 # 避免对零取对数
  }
}

# MCMC参数设置
S <- 50000
burn <- 50000

# 并行环境初始化 ----------------------------------------------------------
cl <- makeCluster(detectCores() - 1)  # 必须在数据初始化之后
registerDoParallel(cl)
clusterEvalQ(cl, {
  sink("NUL")        # Windows
  library(stochvol)
  library(coda)
})

# 并行主循环 --------------------------------------------------------------
result <- foreach(i = 1:N, 
                  .combine = 'cbind',
                  .export = c("S", "burn", "vt", "T"),
                  .errorhandling = "pass") %dopar% {
                    draws <- svsample(vt[,i], draws=S, burnin=burn,
                                      quiet=TRUE, thinpara=10, thinlatent=10)
                    draws$para <- draws$para[[1]]
                    draws$latent <- draws$latent[[1]]
                    k1 <- colMeans(draws$para)
                    k2 <- colMeans(draws$latent)
                    c(k1[1:3], k2)
                  }

# 终止并行环境并保存结果 --------------------------------------------------
stopCluster(cl)
write(t(result), file='svfmeans.txt', ncolumn=dim(result)[2])