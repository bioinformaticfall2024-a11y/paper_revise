def radar_mse_score(mse,mse_min,mse_max):
 if mse_max<=mse_min:raise ValueError('mse_max must be > mse_min')
 return 1.0-(mse-mse_min)/(mse_max-mse_min)
