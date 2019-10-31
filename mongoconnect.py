from pymongo import MongoClient
class Database:

    def __init__(self,ip='localhost',db=None):
        try:
            conn = MongoClient(ip)
            self.db = conn.loco_donor
            print('Connection successful.')
        except:
            print('Error in connection.')
            self.db = None

    def insert_hospital(self, hname, husername, hpassword, hadd, hcity, hstate):
        print("inserting")
        collection = self.db.Hospitals
        a = collection.find( { 'username': { '$exists': True, '$in': [husername]  } } )
        val = []
        for x in a:
            val = x
        if val:
            return False
        else:
            print('No')
            emp_rec1 = {
            "hospital_name": hname,
            "username":husername,
            "password":hpassword,
            "address": hadd,
            "city": hcity,
            "state":hstate,
            "donations":[]
            }
            try:
                rec_id1 = collection.insert_one(emp_rec1)
            except:
                print('Insert error in db.Hospital')

            return True

    def existence(self,username):
        collection = self.db.Donors
        a = collection.find( { 'username': { '$exists': True, '$in': [username]  } } )
        val = []
        for x in a:
            val = x
        if val:
            return False
        else:
            return True

    def insert_donor(self,fn,username,password, fage, fphone, fw, fh, faddress, focc, finfo, fbg, fgen):
        print("inserting")
        collection = self.db.Donors
        a = collection.find( { 'username': { '$exists': True, '$in': [username]  } } )
        val = []
        for x in a:
            val = x
        if val:
            return False
        else:
            emp_rec1 = {
                "name": fn,
                "username":username,
                "password":password,
                "age": fage,
                "phone": fphone,
                "w":fw,
                "h":fh,
                "address":faddress,
                "occupation": focc,
                "Info": finfo,
                "b_g": fbg,
                "Gender": fgen,
                "donations": []
                }
            rec_id1 = collection.insert_one(emp_rec1)
            return True


    def locate(self,fplace,fbg):
        collection = self.db.Donors
        return collection.find({"$and":[{"b_g":{"$eq":fbg}},{"address":{"$regex":fplace}}]})

    def personal_info(self,username):
        collection = self.db.Donors
        return collection.find({"username":username})

    def personal_info_hospital(self,username):
        collection = self.db.Hospitals
        return collection.find({"username":username})

    def login_check(self,username,password):
        collection = self.db.Donors
        myquery = {'username':username,'password':password}
        return collection.find(myquery)

    def login_check_hospital(self,username,password):
        collection = self.db.Hospitals
        myquery = {'username':username,'password':password}
        return collection.find(myquery)

    def add_donation(self,username, date, location, hospital):
        collection = self.db.Donors
        donations = {'date':'', 'location':'', 'hospital_id':''}
        donations['date'] = date
        donations['location'] = location
        donations['hospital_id'] = hospital
        prev_donations = collection.find({'username':username}, {'donations':1})
        for x in prev_donations:
            don_list = x['donations']
        don_list.append(donations)
        collection.update_many({'username':username}, {'$set':{'donations':don_list}})

    def add_donation_hospital(self,username, date, location, donor_id):
        collection = self.db.Hospitals
        donations = {'date':'', 'location':'', 'hospital_id':''}
        donations['date'] = date
        donations['location'] = location
        donations['donor_id'] = donor_id
        prev_donations = collection.find({'username':username}, {'donations':1})
        for x in prev_donations:
            don_list = x['donations']
        don_list.append(donations)
        collection.update_many({'username':username}, {'$set':{'donations':don_list}})
