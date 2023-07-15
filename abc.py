#Importing neccesary packages
import vtk
import sys

#Loading the dataset provided to us:
reader=vtk.vtkXMLImageDataReader()
reader.SetFileName('Isabel_2D.vti')
reader.Update()
data=reader.GetOutput()

#Creating the contour extraction algorithm on our own from scratch:
def Isocontour_Point(point1,point2,value1,value2,threshold,horizontal):
    if value1<value2:
        point1,point2=point2,point1
        value1,value2=value2,value1
    if horizontal==1:
        p1=point1[0]
        p2=point2[0]
        p=(value1-threshold)/(value1-value2)*(p2-p1)+p1
        return (p,point1[1],25.0)
    else:
        p1=point1[1]
        p2=point2[1]
        p=(value1-threshold)/(value1-value2)*(p2-p1)+p1
        return (point1[0],p,25.0)
    
#Creating the function for marching squares algorithm:
def Marching_Squares(data, threshold): 
    iso_contour_lines=vtk.vtkCellArray()
    cell_vtkPoints=vtk.vtkPoints()
    num_of_cells=data.GetNumberOfCells()
    point_ind=0
    
    for i in range(num_of_cells):
        cell=data.GetCell(i)
        cell_points=cell.GetPointIds()
        
        points=[]
        values=[]
        
        for j in range(cell_points.GetNumberOfIds()):
            _id=cell_points.GetId(j)
            points.append(data.GetPoint(_id))
            values.append(data.GetPointData().GetScalars().GetTuple1(_id))
            
        states=[val>threshold for val in values]
        contour_lines=[]
        
        if(states[0]!=states[2]):
            contour_lines.append(Isocontour_Point(points[0],points[2],values[0],values[2],threshold,0))
        if(states[2]!=states[3]):
            contour_lines.append(Isocontour_Point(points[2],points[3],values[2],values[3],threshold,1))
        if(states[3]!=states[1]):
            contour_lines.append(Isocontour_Point(points[3],points[1],values[3],values[1],threshold,0))
        if(states[1]!=states[0]):
            contour_lines.append(Isocontour_Point(points[1],points[0],values[1],values[0],threshold,1))

        if len(contour_lines)==2 or len(contour_lines)==4:
            cell_vtkPoints.InsertNextPoint(contour_lines[0][0],contour_lines[0][1],contour_lines[0][2])
            cell_vtkPoints.InsertNextPoint(contour_lines[1][0],contour_lines[1][1],contour_lines[1][2])
            line1=vtk.vtkLine()
            line1.GetPointIds().SetId(0,point_ind)
            line1.GetPointIds().SetId(1,point_ind+1)
            iso_contour_lines.InsertNextCell(line1)
            point_ind=point_ind+2
            
        if len(contour_lines)==4:
            cell_vtkPoints.InsertNextPoint(contour_lines[2][0],contour_lines[2][1],contour_lines[2][2])
            cell_vtkPoints.InsertNextPoint(contour_lines[3][0],contour_lines[3][1],contour_lines[3][2])
            line2=vtk.vtkLine()
            line2.GetPointIds().SetId(0,point_ind)
            line2.GetPointIds().SetId(1,point_ind+1)
            iso_contour_lines.InsertNextCell(line2)
            point_ind=point_ind+2
    polydata=vtk.vtkPolyData()
    polydata.SetPoints(cell_vtkPoints)  
    polydata.SetLines(iso_contour_lines)
    
    #Creating a vtk PolyData writer
    writer=vtk.vtkXMLPolyDataWriter()
    writer.SetFileName("iso_contour.vtp")
    writer.SetInputData(polydata)
    writer.Write()
    
    return polydata

#Calling the function that we defined above:
polydata=Marching_Squares(data, 270)