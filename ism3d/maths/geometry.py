from matplotlib.path import Path
import numpy as np

def triangle_area(x1, y1, x2, y2, x3, y3):
    """
    calculate area of a triangle
    """
    return abs(0.5*(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2)))

def points_in_triangle(x1, y1, x2, y2, x3, y3,x_arr,y_arr,count=False,method='path'):
    """
    count=True will return point number acount and triangle size
    
    x_arr=np.random.rand(10**6)
    y_arr=np.random.rand(10**6)
    %lprun -f points_in_triangle points_in_triangle(0,0,0,1,1,1,
                                                    x_arr,y_arr,count=True,method='path')
    %lprun -f points_in_triangle points_in_triangle(0,0,0,1,1,1,
                                                    x_arr,y_arr,count=True,method='area')    
    0.035s vs. 0.045s
    """
    # use area.sum method
    if  method.lower()=='area':
        A=triangle_area(x1, y1, x2, y2, x3, y3)
        A1 = triangle_area(x_arr, y_arr, x2, y2, x3, y3) 
        A2 = triangle_area(x1, y1, x_arr, y_arr, x3, y3)
        A3 = triangle_area(x1, y1, x2, y2, x_arr, y_arr)
        if count==True:
            return np.count_nonzero(np.equal(A,A1+A2+A3)),A
        else:
            return np.equal(A,A1+A2+A3)
    
    # use summing method / slightly faster
    if  method.lower()=='path':
        A=triangle_area(x1, y1, x2, y2, x3, y3)
        p=Path([(x1,y1),(x2,y2),(x3,y3)])
        points = np.vstack((x_arr,y_arr)).T
        cc=p.contains_points(points)
        if count==True:
            return cc.sum(),A
        else:
            return cc        
