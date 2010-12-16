from PyFacebook import PyFacebook


class FriendLocation():

    def __init__(self):
        fb = PyFacebook()
        self.graph = fb.graph
        self.locations = {}

    def get_friends(self, uid):
        self.friends = self.graph.get_connections(uid, "friends")['data']

    def get_user(self, uid):
         return self.graph.get_object(uid)

    def add_location(self, user):

        if user.has_key('location'):
            if self.locations.has_key(user['location']['id']):
                self.locations[user['location']['id']]['weight'] += 1
            else:
                self.locations[user['location']['id']] = { 'weight' : 1,
                                                          'name' : user['location']['name']}


    def friends_locations(self, uid):
        
        self.get_friends(uid)

        for item in self.friends:
            user = self.get_user(item['id'])
            self.add_location(user)

        print self.locations




if __name__ == '__main__':
    obj = FriendLocation()
    obj.friends_locations('me')
