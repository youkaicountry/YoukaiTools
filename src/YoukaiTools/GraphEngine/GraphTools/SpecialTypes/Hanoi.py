#void Factory::construct_hanoi (Graph *g, int n, Vertex *varray[3], const wxString &suffix)
def makeHanoi(g, n, xpos = "x", ypos = "y"):
    gl = [ ["", .5, .1], ["", .9, .9], ["", .1, .9] ]
    el = []
    __hanoiRecurse(gl, el, n, [0, 2, 1], "")
    for v in gl:
        g.addVertex(v[0])
        g.setVertexData(v[0], xpos, v[1])
        g.setVertexData(v[0], ypos, v[2])
    for e in el:
        g.addEdge(gl[e[0]][0], gl[e[1]][0])
    return

def __hanoiRecurse(gl, el, n, vertices, suffix):
    
    if n < 1:
        return
    if n == 1:
        #just need to rename vertices and connect edges
        el.append([vertices[0], vertices[1]])
        el.append([vertices[1], vertices[2]])
        el.append([vertices[2], vertices[0]])
        gl[vertices[0]][0] = "0" + suffix
        gl[vertices[1]][0] = "1" + suffix
        gl[vertices[2]][0] = "2" + suffix
        return
    
    x0 = gl[vertices[0]][1]
    x1 = gl[vertices[1]][1]
    x2 = gl[vertices[2]][1]
    y0 = gl[vertices[0]][2]
    y1 = gl[vertices[1]][2]
    y2 = gl[vertices[2]][2]
    v01a = ["", (4.0 * x0 + 3.0 * x1) / 7.0, (4.0 * y0 + 3.0 * y1) / 7.0]
    v01b = ["", (3.0 * x0 + 4.0 * x1) / 7.0, (3.0 * y0 + 4.0 * y1) / 7.0]
    v12a = ["", (4.0 * x1 + 3.0 * x2) / 7.0, (4.0 * y1 + 3.0 * y2) / 7.0]
    v12b = ["", (3.0 * x1 + 4.0 * x2) / 7.0, (3.0 * y1 + 4.0 * y2) / 7.0]
    v20a = ["", (4.0 * x2 + 3.0 * x0) / 7.0, (4.0 * y2 + 3.0 * y0) / 7.0]
    v20b = ["", (3.0 * x2 + 4.0 * x0) / 7.0, (3.0 * y2 + 4.0 * y0) / 7.0]
    l = len(gl)
    gl.append(v01a) #l
    gl.append(v01b) #l+1
    gl.append(v12a) #l+2
    gl.append(v12b) #l+3
    gl.append(v20a) #l+4
    gl.append(v20b) #l+5
    el.extend([[l, l+1], [l+2, l+3], [l+4, l+5]])
    print vertices
    varray0 = [vertices[0], l+5, l]
    varray1 = [l+2, vertices[1], l+1]
    varray2 = [l+3, l+4, vertices[2]]
    
    __hanoiRecurse (gl, el, n - 1, varray0, "0" + suffix)
    __hanoiRecurse (gl, el, n - 1, varray1, "1" + suffix)
    __hanoiRecurse (gl, el, n - 1, varray2, "2" + suffix)
    return