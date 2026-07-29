import re
from decimal import Decimal

def slugify(value:str)->str: return re.sub(r"(^-|-$)","",re.sub(r"[^a-z0-9]+","-",value.lower().strip()))
def product_json(r):
    p,cname,cslug,bname,bslug=r
    return {"id":p.id,"name":p.name,"slug":p.slug,"sku":p.sku,"category":cname,"categorySlug":cslug,"brand":bname,"brandSlug":bslug,"mrp":float(p.mrp or p.price or 0),"price":float(p.sale_price if p.sale_price is not None else p.price or 0),"stock":int(p.stock or 0),"rating":float(p.rating or Decimal('4.4')),"reviews":int(p.reviews or 0),"image":p.image_url or "💊","description":p.description or "","ingredients":p.ingredients or "","dosage":p.dosage or "","warnings":p.warnings or "","featured":bool(p.is_featured),"prescription":bool(p.prescription_required)}
