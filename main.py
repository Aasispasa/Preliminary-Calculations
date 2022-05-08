import math


#################slab inputs###########################
lx=5.135
ly=7.685
lx_dash=2.6

#########################################################

lx1=9.3528
lx2=7.6850
ly1=7.955
ly2=2.6*2




#######################################################
bar_size=20
fck=25
fy=500
#########################################################

def k(fy):
    if fy==250:
        k=0.53
    if fy==415:
        k=0.48
    if fy==500:
        k=0.46
    return k
def cover(exposure):
    if exposure.upper() == "MILD":
        cover=20
    if exposure.upper()=="MODERATE":
        cover=30
    if exposure.upper()=="SEVERE":
        cover=45
    if exposure.upper()=="VERY SEVERE":
        cover=50
    if exposure.upper()=="EXTREME":
        cover=75
    return cover

class deflection_control():

    def __init__(self,dim_1=5,supc="SIMPLY SUPPORTED",pt=0.5,fy=fy,ast_req=1,ast_pro=1,pc=0.05,wwtofw=1,type="beam"):
        self.dim_1=dim_1
        self.supc_1=supc.upper()
        self.pt_1=pt
        self.fy_1=fy
        self.ast_req_1=ast_req
        self.ast_pro_1=ast_pro
        self.pc_1=pc
        self.wwtofw_1=wwtofw
        self.type_1=type.upper()
    
    @property
    def type(self):
        return self.type_1
    
    @type.setter
    def type(self,type_set):
        self.type_1=type_set.upper()

    @property
    def dim(self):
        return self.dim_1

    @dim.setter
    def dim(self,dim_set):
        self.dim_1=dim_set

    
    @property
    def support_condition(self):
        return self.supc_1.upper()

    @support_condition.setter
    def support_condition(self,supc_set):
        self.supc_1=supc_set

        
    @property
    def pt(self):
        return self.pt_1

    @pt.setter
    def pt(self,pt_set):
        self.pt_1=pt_set
    
    @property
    def ast_req(self):
        return self.ast_req_1

    @ast_req.setter
    def ast_req(self,ast_req_set):
        self.ast_req_1=ast_req_set
    
    
    @property
    def ast_pro(self):
        return self.ast_pro_1

    @ast_pro.setter
    def ast_pro(self,ast_pro_set):
        self.ast_pro_1=ast_pro_set
    
    @property
    def fy(self):
        return self.fy_1

    @fy.setter
    def fy(self,fy_set):
        self.fy_1=fy_set
    
    @property
    def pc(self):
        return self.pc_1

    @pc.setter
    def pc(self,pc_set):
        self.pc_1=pc_set
    
    @property
    def web_to_flange(self):
        return self.wwtofw_1

    @web_to_flange.setter
    def web_to_flange(self,wwtofw_set):
        self.wwtofw_1=wwtofw_set

    @property
    def value(self):
        b=1
 
        if self.type=="TWO WAY SLAB":
            if self.dim[0]<3.5 or self.dim[1]<3.5:
                if self.support_condition=="SIMPLY SUPPORTED":
                    if self.fy>250:
                        a=35*0.8
                    else:
                        a=35
                if self.support_condition=="CONTINUOUS":
                    if self.fy>250:
                        a=40*0.8
                    else:
                        a=40
            else:
                if self.support_condition=="CANTILEVER":
                    a=7
                if self.support_condition=="SIMPLY SUPPORTED":
                    a=20
                if self.support_condition=="CONTINUOUS":
                    a=26
        else:
            if self.support_condition=="CANTILEVER":
                a=7
            if self.support_condition=="SIMPLY SUPPORTED":
                a=20
            if self.support_condition=="CONTINUOUS":
                a=26

        if type(self.dim)==list:
            x=self.dim[0]
            y=self.dim[1]
            if x>y:
                check=x
            else:
                check=y
        else:
            check=self.dim
        if check>10:
            b=10/check

        fs=0.58*self.fy*self.ast_req/self.ast_pro
        c=min(abs(1/(0.225+0.0032*fs-0.625*math.log10(1/self.pt))),2)
        d=min(max(1.6*self.pc/(self.pc+0.275),1),1.5)
        e=0.8+(0.2/0.7)*(self.web_to_flange-0.3)
        return a*b*c*d*e


def slab_design(lx,ly,support='Continuous'):
    if lx > ly:
        lx,ly=ly,lx
    s=deflection_control()
    s.pt=0.15

    count=0

    if lx > ly:
        lx,ly=ly,lx

    s.dim=[lx,ly]

    if (ly/lx) > 2:
        s.type="one way slab"
        s.support_condition=support
    else:
        s.type="two way slab"
        s.support_condition=support
    d=(lx/s.value)*1000
    D=math.ceil((d+bar_size/2+cover("mild"))/10)*10
    if D>125:
        ly=ly/2
        if lx > ly:
            lx,ly=ly,lx
        s.dim=[lx,ly]
        if (ly/lx) > 2:
            s.type="one way slab"
            s.support_condition=support        
        else:
            s.type="two way slab"
            s.support_condition=support
        d=(lx/s.value)*1000
        D=math.ceil((d+bar_size/2+cover("mild"))/10)*10
        count=1

    

    return D,count

def beam_design(lx,ly,lx_dash=lx,wid=0.23,slab_D=150,secondary_beam=1,support="Simply Supported"):
    
    if lx > ly:
        lx,ly=ly,lx
    l=ly
    b=deflection_control()
    b.type='beam'
    b.pt=2.5
    b.pc=0.5
    d=(l/b.value)*1000
    D=math.ceil((d+bar_size/2+cover("mild"))/10)*10

    slab_a=(lx*ly/2)+(lx_dash*ly/2)-((lx/2)**2+(lx_dash/2)**2)
    slab_wt=25*slab_a*slab_D/1000
    dl_screed=21*0.025*slab_a
    dl_floor=26*0.025*slab_a
    dl_plaster=20.4*0.0125*slab_a
    dl_beam=25*secondary_beam*(lx+lx_dash)*0.23*0.23/2
    ll=2*slab_a
    fl=1.5*(dl_beam+dl_floor+dl_plaster+dl_screed+ll+slab_wt)
    w=fl/ly
    mu=w*(ly**2)/8
    d_dash=(math.sqrt(mu/(0.36*fck*1000*k(fy)*(1-0.42*k(fy))*wid)))*1000
    D_dash=math.ceil((d_dash+bar_size/2+cover("mild"))/10)*10


    return max(D,D_dash)


def column_design(lx1,ly1,lx2,ly2,slab_D=160,beam_D=700,floor_ht=4.65,wall_len=10,floor_no=2):
    slab_a=(lx1+lx2)*(ly1+ly2)/4
    slab_wt=25*slab_a*slab_D/1000
    dl_screed=21*0.025*slab_a
    dl_floor=26*0.025*slab_a
    dl_plaster=20.4*0.0125*slab_a
    dl_beam=(lx1+lx2+ly1+ly2)*beam_D*0.23*25/4000*1.25
    ll=2*slab_a
    wl=0.115*20*floor_ht*wall_len
    fl=1.5*(dl_beam+dl_floor+dl_plaster+dl_screed+ll+slab_wt+wl)*floor_no
    Ag=(1.25*fl*1000)/(0.4*fck*0.985+0.67*fy*0.015)
    return round(math.sqrt(Ag)/10)*10


print(slab_design(lx,ly))
print(beam_design(lx,ly))
print(column_design(lx1,ly1,lx2,ly2))

# print(s.value)
